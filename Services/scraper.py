import configparser
import time
import os
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import Services.consts as consts
from Entities.match import Match, Team, Sport
from Entities.player import Player, Position, IHGoalkeeper, Squad


def clean_url_new_style(url: str) -> str:
    """Remove query parameters and the 'summary' segment from a URL if present."""

    # Remove query parameters by splitting at the first '?' and taking the part before it
    url_no_params = url.split('?')[0]

    # Split the URL path into segments by '/'
    parts = url_no_params.split('/')

    # If 'summary' segment exists, remove it and everything after
    if 'summary' in parts:
        index = parts.index('summary')
        cleaned_url = '/'.join(parts[:index]) + '/'
    else:
        cleaned_url = url_no_params

    return cleaned_url


class Scraper:
    """
    Static class to get an information from a web-page.
    """

    @staticmethod
    def __create_driver():
        """
        Creates and returns a driver for scraping.

        :return: Chrome's webdriver.
        """

        # set settings for a driver
        options = Options()
        options.headless = True
        options.add_argument(consts.USER_AGENT_FULL)
        options.add_argument("window-size=1920,1080")
        options.add_argument('--log-level=3')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        options.add_argument("--headless=new")

        # get a path of ChromeDriver from
        config = configparser.ConfigParser()
        try:
            config.read('settings.ini')
            path_for_driver = config['COMMON']['SELENIUM_DRIVER_PATH']
        except:
            config.read('../settings.ini')
            path_for_driver = config['COMMON']['SELENIUM_DRIVER_PATH']

        return webdriver.Chrome(executable_path=path_for_driver, options=options)

    @staticmethod
    def get_match(url: str) -> Match:
        """
        Gets a sport match by URL.

        :param url: URL of sport match.
        :return: type of Match.
        """
        match = None

        # get a URL for lineups of match

        # OLD VERSION
        # url_lineups = url.split('#')[0] + '#' + consts.FLASHSCORE_SUFFIX_FOR_LINEUPS
        # NEW VERSION
        url_lineups = clean_url_new_style(url) + consts.FLASHSCORE_SUFFIX_FOR_LINEUPS_NEW

        # get a web-page with lineups
        driver = Scraper.__create_driver()
        driver.get(url_lineups)
        driver.implicitly_wait(10)

        nav_sport_tournament = driver.find_element_by_xpath('//ol[contains(@class, "wcl-breadcrumbList")]')

        # get sport
        sport_name = str(nav_sport_tournament.find_element_by_xpath('.//li[1]/a/span').text).lower().\
            capitalize()
        if sport_name == Sport.football.value:
            sport = Sport.football
        elif sport_name == Sport.hockey.value:
            sport = Sport.hockey
        # finishes if not football or hockey
        else:
            driver.quit()
            return None

        # get tournament name
        tournament_name = str(nav_sport_tournament.find_element_by_xpath('.//li[2]/a/span').text).lower().capitalize()

        # get boxes with lineups
        boxes_lineups = driver.find_elements_by_xpath('//div[@class="lf__lineUp"]/div[@class="section"]')

        # if lineups are ready
        if boxes_lineups:
            # get a URLs of teams
            url_team_a = driver.find_element_by_xpath('//div[@class="duelParticipant"]/div[2]/a').get_attribute('href')
            url_team_b = driver.find_element_by_xpath('//div[@class="duelParticipant"]/div[4]/a').get_attribute('href')

            # get teams
            team_a = Scraper.__get_team(url_team_a + consts.FLASHSCORE_SQUAD)
            team_b = Scraper.__get_team(url_team_b + consts.FLASHSCORE_SQUAD)

            # get lineups for both teams
            data_lineups = Scraper.__get_lineups_for_both(driver)
            team_a_lineup = data_lineups[0]
            team_b_lineup = data_lineups[1]
            # mark players of teams by info about lineups
            team_a.mark_players_info_squad(team_a_lineup)
            team_b.mark_players_info_squad(team_b_lineup)

            # get lineup of last match
            team_a_lineup_lastm = Scraper.__get_lineup_last_match(url_team_a + consts.FLASHSCORE_RESULTS, team_a.name, sport)
            team_b_lineup_lastm = Scraper.__get_lineup_last_match(url_team_b + consts.FLASHSCORE_RESULTS, team_b.name, sport)
            # mark players of teams by info about last match lineups
            team_a.mark_players_info_squad_last_match(team_a_lineup_lastm)
            team_b.mark_players_info_squad_last_match(team_b_lineup_lastm)

            # create match
            match = Match(sport, url, tournament_name, team_a, team_b)

        # if lineups are not ready then return match with empty lists of players for both teams
        else:
            team_a_name = driver.find_element_by_xpath('//div[@class="duelParticipant"]/div[2]/div[3]').text
            team_b_name = driver.find_element_by_xpath('//div[@class="duelParticipant"]/div[4]/div[3]').text
            match = Match(sport, url, tournament_name, Team(team_a_name, None, None), Team(team_b_name, None, None))

        driver.quit()

        return match

    @staticmethod
    def __get_players(driver: webdriver.Chrome, elements: list) -> list:
        """
        Gets list of players from web-element. Using to get an information about lineup.

        :param driver: ChromeDriver of a match for which driving the browser at the moment.
        :param elements: list of web-elements.
        :return: list of players from web-elements.
        """
        def clean_player_name(name: str) -> str:
            name = name.replace('(G)', '').replace('(C)', '').replace('(A)', '').strip()
            if name.endswith('.'):
                name = name[:-1]
            return name

        def append_player(players_list, name, url=None):
            if url and not url.endswith('/'):
                url += '/'
            if url:
                players_list.append(Player(name, url, None, None, None, None, None, None))
            else:
                players_list.append(name)

        players = []

        driver.implicitly_wait(1.5)
        new_style = bool(elements and elements[0].find_elements_by_xpath('.//button'))

        for element in elements:
            if new_style:
                try:
                    # New style with button of player profile (actualy for football)
                    button = element.find_element_by_xpath('.//button')
                    name = element.find_element_by_xpath('.//button/strong').text
                    name = clean_player_name(name)

                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    driver.execute_script("arguments[0].click();", button)

                    widget = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((
                                    By.XPATH,
                                    '//div[@data-analytics-context="widget-player-match-stats-card"]'
                                ))
                            )

                    url = widget.find_element_by_xpath('.//div/a').get_attribute('href')
                    append_player(players, name, url)

                    button_close = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH,
                            '//button[@data-testid="wcl-dialogCloseButton"]'
                        ))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", button_close)
                    driver.execute_script("arguments[0].click();", button_close)

                except NoSuchElementException:
                    continue

            else:
                # Old style (actually for hockey)
                try:
                    a_tag = element.find_element_by_xpath('.//a')
                    name = a_tag.text
                    url = a_tag.get_attribute('href')

                    name = clean_player_name(name)
                    append_player(players, name, url)

                except NoSuchElementException:
                    try:
                        name = element.find_element_by_xpath('./div[3]').text
                        name = clean_player_name(name)
                        players.append(name)
                    except NoSuchElementException:
                        continue
        return players

    @staticmethod
    def __get_lineups_for_both(driver: webdriver.Chrome) -> tuple:
        """
        Gets an information about lineups for both team.

        :param driver: ChromeDriver of a match for which driving the browser at the moment.
        :return: tuple (team_a_info, team_b_info) of tuples (team__xi, team__sub) with list of players.
        """

        team_a_xi, team_a_sub = [], []
        team_b_xi, team_b_sub = [], []

        # get sections with info about lineups
        sections = driver.find_elements_by_xpath('//div[@class="lf__lineUp"]/div[@class="section"]')
        # get info
        for section in sections:
            section_description = section.find_element_by_xpath('./div[1]').text
            # in XI
            if section_description in consts.LINEUPS_DESCRIPTIONS_XI:
                sides = section.find_elements_by_xpath('./div[@class="lf__sidesBox"]/div/div[@class="lf__side"]')

                # get for home
                team_a_xi.extend(Scraper.__get_players(driver, sides[0].find_elements_by_xpath('./div')))
                # get for away
                team_b_xi.extend(Scraper.__get_players(driver, sides[1].find_elements_by_xpath('./div')))

            # on sub
            elif section_description in consts.LINEUPS_DESCRIPTIONS_SUB:
                sides = section.find_elements_by_xpath('./div[@class="lf__sidesBox"]/div/div[@class="lf__side"]')

                # get for home
                team_a_sub.extend(Scraper.__get_players(driver, sides[0].find_elements_by_xpath('./div')))
                # get for away
                team_b_sub.extend(Scraper.__get_players(driver, sides[1].find_elements_by_xpath('./div')))

        team_a_info = (team_a_xi, team_a_sub)
        team_b_info = (team_b_xi, team_b_sub)
        return (team_a_info, team_b_info)

    @staticmethod
    def __get_lineup_last_match(url: str, team_name: str, sport: Sport) -> tuple:
        """
        Gets an information about lineup of last match for a team.

        :param url: URL of team results.
        :param team_name: name of team.
        :param sport: type Sport.
        :return: tuple with lists of players which were in lineup of last match.
        """

        last_match_players = None

        # get a web-page about a team
        driver = Scraper.__create_driver()
        driver.get(url)
        driver.implicitly_wait(10)

        # get list of URL's of last matches

        if sport == Sport.football:
            last_matches = driver.find_elements_by_xpath('//div[contains(@class, "leagues--static event--leagues")]/div/div')
        else:
            last_matches = driver.find_elements_by_xpath('//div[contains(@class, "leagues--static event--leagues")]/div')

        for lm in last_matches:
            match_id = lm.get_attribute('id').split('_')[-1]
            if not match_id:
                continue

            # OLD VERSION
            # url_lm = consts.FLASHSCORE_MAIN + lm.get_attribute('id').split('_')[-1] + '/#' \
            #         + consts.FLASHSCORE_SUFFIX_FOR_LINEUPS
            # NEW VERSION
            url_lm = lm.find_element_by_xpath('.//a').get_attribute('href')
            url_lm = clean_url_new_style(url_lm) + consts.FLASHSCORE_SUFFIX_FOR_LINEUPS_NEW

            last_match_players = Scraper.__get_lineup_for_team(url_lm, team_name)
            if last_match_players and last_match_players[0] and last_match_players[1]:
                break

        driver.quit()

        if last_match_players is None:
            # no information about lineup of last match
            last_match_players = ([], [])

        return last_match_players

    @staticmethod
    def __get_lineup_for_team(url: str, team_name: str) -> list:
        """
        Gets an information about lineup of match for a team.

        :param url: URL of a match.
        :param team_name: name of team.
        :return: tuple (team_xi, team_sub) with lists of players which were in XI/Sub.
        """

        team_xi, team_sub = [], []

        # get a web-page about a match
        driver = Scraper.__create_driver()
        driver.get(url)
        driver.implicitly_wait(10)

        # find out that team was at home or away to get needed lineup
        home_team_name = driver.find_element_by_xpath('//div[@class="duelParticipant"]/div[2]/div[3]/div/a').text
        index = 0 if team_name == home_team_name else 1

        try:
            # get sections with info about lineups
            sections = driver.find_elements_by_xpath('//div[@class="lf__lineUp"]/div[@class="section"]')
            # get info
            for section in sections:
                section_description = section.find_element_by_xpath('./div[1]').text
                # in XI
                if section_description in consts.LINEUPS_DESCRIPTIONS_XI:
                    sides = section.find_elements_by_xpath('./div[@class="lf__sidesBox"]/div/div[@class="lf__side"]')
                    # get players
                    team_xi.extend(Scraper.__get_players(driver, sides[index].find_elements_by_xpath('./div')))

                # on sub
                elif section_description in consts.LINEUPS_DESCRIPTIONS_SUB:
                    sides = section.find_elements_by_xpath('./div[@class="lf__sidesBox"]/div/div[@class="lf__side"]')
                    # get players
                    team_sub.extend(Scraper.__get_players(driver, sides[index].find_elements_by_xpath('./div')))

            return (team_xi, team_sub)
        except NoSuchElementException:
            return None
        finally:
            driver.quit()

    @staticmethod
    def __get_team(url: str) -> Team:
        """
        Gets a team by URL.

        :param url: URL of a team.
        :return: type of Team.
        """
        team = None

        # get a web-page with squad
        driver = Scraper.__create_driver()
        driver.get(url)
        driver.implicitly_wait(10)

        # get sport name
        sport_name = str(driver.find_element_by_xpath('//a[@class="breadcrumb__link"]').text).lower().capitalize()

        # get team name
        team_name = driver.find_element_by_xpath('//div[@class="heading__title"]/div[@class="heading__name"]').text

        # get team logo if not exits
        logo_name = f'Logos/{sport_name}_{team_name.replace(" ", "_").replace("/", "_")}.png'
        #logo_name = f'../Logos/{sport_name}_{team_name.replace(" ", "_").replace("/", "_")}.png'
        if not os.path.isfile(logo_name):
            logo_path = driver.find_element_by_xpath('//div[@class="heading"]/img').get_attribute('src')
            Scraper.__save_logo(logo_path, logo_name)
        team = Team(team_name, url.replace(consts.FLASHSCORE_SQUAD, ''), logo_name)

        # if hockey then need to get an info about goalkeepers from main page (not Total)
        if sport_name == Sport.hockey.value:
            # get boxes with positions
            position_boxes = driver.find_elements_by_xpath('//div[@class="squad-table profileTable"]/div')
            # get list of players
            for box in position_boxes:
                position_name = box.find_element_by_xpath('./div[@class="lineupTable__title"]').text
                if position_name not in Position.get_names():
                    continue
                if position_name == Position.Goalkeepers.name:
                    # get info about player
                    rows = box.find_elements_by_xpath('./div[@class="lineupTable__row"]')
                    for row in rows:
                        try:
                            number = int(row.find_element_by_xpath('./div[1]').text)
                        except ValueError:
                            number = None
                        nationality = row.find_element_by_xpath('./div[2]/div[1]').get_attribute('title')
                        pl_name = row.find_element_by_xpath('./div[2]/div[2]/a').text
                        pl_url = row.find_element_by_xpath('./div[2]/div[2]/a').get_attribute('href')
                        try:
                            age = int(row.find_element_by_xpath('./div[3]').text)
                        except ValueError:
                            age = None
                        matches_played = int(row.find_element_by_xpath('./div[4]').text)
                        try:
                            sv = float(row.find_element_by_xpath('./div[5]').text)
                        except ValueError:
                            sv = -1
                        try:
                            gaa = float(row.find_element_by_xpath('./div[6]').text)
                        except ValueError:
                            gaa = -1
                        try:
                            so = int(row.find_element_by_xpath('./div[7]').text)
                        except ValueError:
                            so = -1
                        player = IHGoalkeeper(pl_name, pl_url, nationality, number, age, Position.Goalkeepers,
                                              matches_played, sv, gaa, so)
                        team.add_player(player)
                else:
                    break

        # get section with filter of matches played
        if sport_name == Sport.football.value:
            xpath_query = '//div[@class="filter lineup__filter"]/div[@class="filter__group"]'
        else:
            xpath_query = '//div[@class="lineup"]/*/div[@class="filter lineup__filter"]/div[@class="filter__group"]'
        filter_group = driver.find_element_by_xpath(xpath_query)

        # scroll window of browser to this section
        driver.execute_script("arguments[0].scrollIntoView(true);", filter_group)
        # switch to 'Total'
        buttons = filter_group.find_elements_by_xpath('.//button')
        for group in buttons:
            if group.text.strip() == 'TOTAL' or group.text.strip() == 'Total':
                driver.execute_script("arguments[0].click();", group)

        # get boxes with positions
        position_boxes = driver.find_elements_by_xpath('//div[@id="overall-all-table"]/div')
        # get list of players
        for box in position_boxes:
            position_name = box.find_element_by_xpath('./div[@class="lineupTable__title"]').text
            if position_name not in Position.get_names():
                continue

            if position_name == Position.Goalkeepers.name:
                pl_position = Position.Goalkeepers
            elif position_name == Position.Defenders.name:
                pl_position = Position.Defenders
            elif position_name == Position.Midfielders.name:
                pl_position = Position.Midfielders
            elif position_name == Position.Forwards.name:
                pl_position = Position.Forwards
            else:
                pl_position = Position.Unknown

            # get info about player
            rows = box.find_elements_by_xpath('./div[@class="lineupTable__row"]')
            for row in rows:
                try:
                    number = int(row.find_element_by_xpath('./div[1]').text)
                except ValueError:
                    number = None
                nationality = row.find_element_by_xpath('./div[2]/div[1]').get_attribute('title')
                pl_name = row.find_element_by_xpath('./div[2]/div[2]/a').text
                pl_url = row.find_element_by_xpath('./div[2]/div[2]/a').get_attribute('href')
                try:
                    age = int(row.find_element_by_xpath('./div[3]').text)
                except ValueError:
                    age = None
                matches_played = int(row.find_element_by_xpath('./div[4]').text)

                if sport_name == Sport.hockey.value and pl_position == Position.Goalkeepers:
                    try:
                        sv = float(row.find_element_by_xpath('./div[5]').text)
                    except ValueError:
                        sv = -1
                    try:
                        gaa = float(row.find_element_by_xpath('./div[6]').text)
                    except ValueError:
                        gaa = -1
                    try:
                        so = int(row.find_element_by_xpath('./div[7]').text)
                    except ValueError:
                        so = -1
                    player = IHGoalkeeper(pl_name, pl_url, nationality, number, age, Position.Goalkeepers,
                                          matches_played, sv, gaa, so)
                    if player not in team.players:
                        team.add_player(player)
                else:
                    if sport_name == Sport.football.value:
                        goals_scored = int(row.find_element_by_xpath('./div[6]').text)
                    else:
                        goals_scored = int(row.find_element_by_xpath('./div[5]').text)
                    player = Player(pl_name, pl_url, nationality, number, age, pl_position, matches_played, goals_scored)
                    team.add_player(player)

        driver.quit()

        return team

    @staticmethod
    def __save_logo_v2(url: str, name: str) -> None:
        """
        Saves team logo by a URL.

        :param url: URL of a logo.
        :param name: to save a logo by this name.
        """

        driver = Scraper.__create_driver()
        driver.get(url)
        driver.implicitly_wait(2)

        with open(name, 'wb') as file:
            l = driver.find_element_by_xpath('//img')
            file.write(l.screenshot_as_png)

        driver.quit()

    @staticmethod
    def __save_logo(url: str, name: str) -> None:
        """
        Saves team logo by a URL.

        :param url: URL of a logo.
        :param name: to save a logo by this name.
        """
        response = requests.get(url, stream=True)
        with open(name, 'wb') as outfile:
            shutil.copyfileobj(response.raw, outfile)
        del response
