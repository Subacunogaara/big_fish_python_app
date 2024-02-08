import flet as ft
import looker_sdk

sdk = looker_sdk.init40()


def main(page: ft.Page):
    page.title = "BigFishGames"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 820
    page.window_height = 800
    page.scroll = "always"



    '''Change the theme of working window'''

    def change_theme(a):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    app_theme = ft.Row(
        [
            ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
            ft.Text('Theme')
        ],
        alignment=ft.MainAxisAlignment.END
    )


    '''Check the single dashboard + checking function'''

    user_dashboard_data = ft.TextField(label='Enter dashboard id', width=170)
    user_look_data = ft.TextField(label='Enter look id', width=120)
    result_list_links = ft.ListView(expand=True, spacing=5)

    def open_url(e):
        page.launch_url(e.data)

    def single_dashboard_check(id, file=False):
        if file == False:
            id = user_dashboard_data.value
        try:
            board = sdk.dashboard(dashboard_id=id)
            error_words = ('error', 'Error', 'trouble', 'Trouble')
            for tile in board.dashboard_elements:
                query = tile.query
                if query and query.id:
                    query_response = sdk.run_query(query_id=query.id, result_format='json')
                    if any(word in query_response for word in error_words):
                        result_list_links.controls.append(ft.Row([
                            ft.Markdown(
                                f"[https://bigfishgames.gw1.cloud.looker.com/dashboards/{id}](https://bigfishgames.gw1.cloud.looker.com/dashboards/{id})",
                                on_tap_link=open_url,
                                expand=False),
                            ft.Icon(ft.icons.ERROR, color='red'),
                            ft.Text(f'{board.title}')], alignment=ft.MainAxisAlignment.START))
                        page.update()
                        break
            else:
                result_list_links.controls.append(ft.Row([
                    ft.Markdown(
                        f"[https://bigfishgames.gw1.cloud.looker.com/dashboards/{id}](https://bigfishgames.gw1.cloud.looker.com/dashboards/{id})",
                        on_tap_link=open_url,
                        expand=False),
                    ft.Icon(ft.icons.DONE, color='green'),
                    ft.Text(f'{board.title}')], alignment=ft.MainAxisAlignment.START))
                page.update()
        except:
            result_list_links.controls.append(ft.Row([
                ft.Markdown(
                    f"[https://bigfishgames.gw1.cloud.looker.com/dashboards/{id}](https://bigfishgames.gw1.cloud.looker.com/dashboards/{id})",
                    on_tap_link=open_url,
                    expand=False),
                ft.Icon(ft.icons.ERROR, color='red')
            ], alignment=ft.MainAxisAlignment.START)
            )
            page.update()


    def single_look_check(id, file=False):
        if file == False:
            id = user_look_data.value
        try:
            look = sdk.look(look_id=id)
            error_words = ('error', 'Error', 'trouble', 'Trouble')
            query = look.query
            if query and query.id:
                query_response = sdk.run_query(query_id=query.id, result_format='json')
                if any(word in query_response for word in error_words):
                    result_list_links.controls.append(ft.Row([
                        ft.Markdown(
                            f"[https://bigfishgames.gw1.cloud.looker.com/looks/{id}](https://bigfishgames.gw1.cloud.looker.com/looks/{id})",
                            on_tap_link=open_url,
                            expand=False),
                        ft.Icon(ft.icons.ERROR, color='red'),
                        ft.Text(f'{look.title}')], alignment=ft.MainAxisAlignment.START))
                    page.update()
                else:
                    result_list_links.controls.append(ft.Row([
                        ft.Markdown(
                            f"[https://bigfishgames.gw1.cloud.looker.com/looks/{id}](https://bigfishgames.gw1.cloud.looker.com/looks/{id})",
                            on_tap_link=open_url,
                            expand=False),
                        ft.Icon(ft.icons.DONE, color='green'),
                        ft.Text(f'{look.title}')], alignment=ft.MainAxisAlignment.START))
                    page.update()
        except:
            result_list_links.controls.append(ft.Row([
                ft.Markdown(
                    f"[https://bigfishgames.gw1.cloud.looker.com/look/{id}](https://bigfishgames.gw1.cloud.looker.com/look/{id})",
                    on_tap_link=open_url,
                    expand=False),
                ft.Icon(ft.icons.ERROR, color='red')
            ], alignment=ft.MainAxisAlignment.START)
            )
            page.update()

    button_for_single_dash = ft.ElevatedButton(text='Check dashboard', height=50, on_click=single_dashboard_check)
    button_for_single_look = ft.ElevatedButton(text='Check look', height=50, on_click=single_look_check)



    # '''Check the list of dashboards from file'''

    # file_picker = ft.FilePicker()
    # page.overlay.append(file_picker)
    # button_for_file_picker = ft.ElevatedButton("Choose file",
    #                                                 on_click=lambda _: file_picker.pick_files(allow_multiple=False))

    # def check_from_file(d):
    #     list_of_dashboards = []
    #     with open('dashboards.txt') as file:
    #         for line in file:
    #             list_of_dashboards.append(line.strip())
    #
    #     for id in list_of_dashboards:
    #         single_check(id, file=True)
    #
    #     result_list_links.controls.append(ft.Text('DONE!'))
    #
    #     page.update()
    #
    # button_for_file = ft.ElevatedButton(text='Check all Dashboards from file', height=50, on_click=check_from_file)

    def get_dashboards_in_folder(folder_id, dict_of_ids):
        dashboards = sdk.folder_dashboards(folder_id)
        for dashboard in dashboards:
            dict_of_ids['dashboards'].append(dashboard.id)

        looks = sdk.folder_looks(folder_id)
        for look in looks:
            dict_of_ids['looks'].append(look.id)

        subfolders = sdk.folder_children(folder_id)
        for folder in subfolders:
            if 'archive' not in folder.name.lower():
                get_dashboards_in_folder(folder.id, dict_of_ids)


    '''Check the all Dashboards from Checkbox List'''

    check_executive = ft.Checkbox(label='Executive KPIs', value=True)
    check_ltv = ft.Checkbox(label='Cohort LTV KPIs', value=True)
    check_ad_mon = ft.Checkbox(label='Ad Monetization', value=True)
    check_all_games = ft.Checkbox(label='All Games', value=True)

    check_blast_explorers = ft.Checkbox(label='Blast Explorers', value=False)
    check_cooking_craze = ft.Checkbox(label='Cooking Craze', value=False)
    check_evermerge = ft.Checkbox(label='Evermerge', value=False)
    check_fairway = ft.Checkbox(label='Fairway', value=False)
    check_fashion = ft.Checkbox(label='Fashion Crafters', value=False)
    check_gummy_drop = ft.Checkbox(label='Gummy Drop!', value=False)
    check_match_upon_a_time = ft.Checkbox(label='Match Upon a Time', value=False)
    check_PnP = ft.Checkbox(label='Puzzles and Passports', value=False)
    check_towers_and_titans = ft.Checkbox(label='Towers & Titans', value=False)
    check_travel_crush = ft.Checkbox(label='Travel Crush', value=False)
    check_ultimate_survivors = ft.Checkbox(label='Ultimate Survivors', value=False)


    def show_hide_games(x):
        check_all_games.value = False
        check_all_games.disabled = True

        if len(forth_row.controls) == 0:
            forth_row.controls = [check_blast_explorers,
                                  check_cooking_craze,
                                  check_evermerge,
                                  check_fairway,
                                  check_fashion,
                                  check_gummy_drop
                                  ]
            fifth_row.controls = [check_match_upon_a_time,
                                  check_PnP,
                                  check_towers_and_titans,
                                  check_travel_crush,
                                  check_ultimate_survivors
                                  ]
        else:
            check_all_games.value = True
            check_all_games.disabled = False
            forth_row.controls = []
            fifth_row.controls = []
        page.update()

    games_selected_button = ft.ElevatedButton(text='Show games', height=50, on_click=show_hide_games)


    def check_all_marked(y):
        pb = ft.ProgressBar(width=200)
        if len(third_row.controls) == 3:
            third_row.controls.extend((pb, ft.Text('Processing...', color='blue')))
        else:
            for i in range(len(third_row.controls) - 3):
                third_row.controls.pop()
            third_row.controls.extend((pb, ft.Text('Processing...', color='blue')))
        page.update()

        folders_dict = {'Executive KPIs': '1121',
                        'Cohort LTV KPIs': '333',
                        'Ad Monetization': '400',
                        'All Games': '399',
                        'Blast Explorers': '889',
                        'Cooking Craze': '59',
                        'Evermerge': '870',
                        'Fairway': '1128',
                        'Fashion Crafters': '763',
                        'Gummy Drop!': '58',
                        'Match Upon a Time': '1035',
                        'Puzzles and Passports': '1161',
                        'Towers & Titans': '844',
                        'Travel Crush': '1074',
                        'Ultimate Survivors': '1043'}

        main_marked_list = (check_executive,
                            check_ltv,
                            check_ad_mon
                            )
        games_marked_list = (check_blast_explorers,
                             check_cooking_craze,
                             check_evermerge,
                             check_fairway,
                             check_fashion,
                             check_gummy_drop,
                             check_match_upon_a_time,
                             check_PnP,
                             check_towers_and_titans,
                             check_travel_crush,
                             check_ultimate_survivors)

        list_of_folders = []
        for v in main_marked_list:
            if v.value:
                list_of_folders.append(folders_dict[v.label])

        if check_all_games.value:
            list_of_folders.append(folders_dict['All Games'])
        else:
            for game in games_marked_list:
                if game.value:
                    list_of_folders.append(folders_dict[game.label])

        dict_of_dashboards_and_looks = {'dashboards': [], 'looks': []}
        for folder in list_of_folders:
            get_dashboards_in_folder(folder, dict_of_dashboards_and_looks)

        pb_step = round(1 / (len(dict_of_dashboards_and_looks['dashboards']) + len(dict_of_dashboards_and_looks['looks'])), 2)
        pb.value = 0
        page.update()


        for id in dict_of_dashboards_and_looks['dashboards']:
            single_dashboard_check(id, file=True)
            pb.value += pb_step
            page.update()

        for id in dict_of_dashboards_and_looks['looks']:
            single_look_check(id, file=True)
            pb.value += pb_step
            page.update()

        for i in range(len(third_row.controls) - 3):
            third_row.controls.pop()
        third_row.controls.extend((ft.Text('DONE !!!', color='green'),))
        page.update()

    button_for_all_dashboards_in_looker = ft.ElevatedButton(text='Check all marked Dashboards', height=50, on_click=check_all_marked)



    '''Check the list of dashboards from Looker folder'''

    user_data_folder = ft.TextField(label='Enter folder id', width=170)

    def check_from_folder(d):
        dict_of_dashs_and_looks = {'dashboards': [], 'looks': []}
        pb = ft.ProgressBar(width=200)
        third_row = ft.Row([button_for_all_dashboards_in_looker, games_selected_button, check_all_games])
        third_row.controls.extend((pb, ft.Text('Processing...', color='blue')))
        page.update()

        get_dashboards_in_folder(user_data_folder.value, dict_of_dashs_and_looks)

        pb_step = round(1/(len(dict_of_dashs_and_looks['dashboards']) + len[dict_of_dashs_and_looks['looks']]), 2)
        pb.value = 0

        for id in dict_of_dashs_and_looks['dashboards']:
            single_dashboard_check(id, file=True)
            pb.value += pb_step
            page.update()

        for id in dict_of_dashs_and_looks['looks']:
            single_look_check(id, file=True)
            pb.value += pb_step
            page.update()

        for i in range(len(third_row.controls) - 3):
            third_row.controls.pop()
        third_row.controls.extend((ft.Text('DONE !!!', color='green'),))

        page.update()

    button_for_folder = ft.ElevatedButton(text='Check all from folder', height=50, on_click=check_from_folder)



    '''First page'''

    def clean_list(x):
        result_list_links.controls = []
        page.update()

    clean_button = ft.ElevatedButton(text='Clean List', height=50, on_click=clean_list)

    first_row = ft.Row([user_dashboard_data, button_for_single_dash, user_look_data, button_for_single_look, clean_button])
    second_row = ft.Row([user_data_folder, button_for_folder, check_executive, check_ltv, check_ad_mon])
    third_row = ft.Row([button_for_all_dashboards_in_looker, games_selected_button, check_all_games])
    forth_row = ft.Row([])
    fifth_row = ft.Row([])
    dashboard_check = ft.Column(
        [
            first_row,
            second_row,
            third_row,
            forth_row,
            fifth_row,
            ft.Row(
                [
                    result_list_links,
                ]
            )
        ]
    )



    '''Second Page'''

    bed = ft.Row(
        [ft.Icon(ft.icons.BED),
         ft.Text('In developing')]
    )



    '''Navigation bar in the bottom of the app'''

    def navigate(b):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0:
            page.add(app_theme)
            page.add(dashboard_check)
        elif index == 1:
            page.add(app_theme)
            page.add(bed)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label='Dashboard Check'),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label='User Mirroring'),
        ],
        on_change=navigate
    )

    page.add(app_theme)
    page.add(dashboard_check)


ft.app(target=main)
