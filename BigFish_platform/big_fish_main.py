import flet as ft
import looker_sdk

sdk = looker_sdk.init40()


def main(page: ft.Page):
    page.title = "BigFishGames"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 700
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

    '''Check the single dashboard'''
    user_data = ft.TextField(label='Enter dashboard id', width=400)
    result_list_links = ft.ListView(expand=True, spacing=5)

    def open_url(e):
        page.launch_url(e.data)

    def single_check(id, file=False):
        if file == False:
            id = user_data.value
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
        except Exception:
            result_list_links.controls.append(ft.Row([
                ft.Markdown(
                    f"[https://bigfishgames.gw1.cloud.looker.com/dashboards/{id}](https://bigfishgames.gw1.cloud.looker.com/dashboards/{id})",
                    on_tap_link=open_url,
                    expand=False),
                ft.Icon(ft.icons.ERROR, color='red'),
                ft.Text(f'{sdk.dashboard(dashboard_id=id).title}')], alignment=ft.MainAxisAlignment.START))
            page.update()

    button_for_single_dash = ft.ElevatedButton(text='Check dashboard', height=50, on_click=single_check)

    '''Check the list of dashboards from file'''

    def check_from_file(d):
        list_of_dashboards = []
        with open('dashboards.txt') as file:
            for line in file:
                list_of_dashboards.append(line.strip())

        for id in list_of_dashboards:
            single_check(id, file=True)

        result_list_links.controls.append(ft.Text('DONE!'))

        page.update()

    button_for_file = ft.ElevatedButton(text='Check all Dashboards from file', height=50, on_click=check_from_file)

    '''Check the all Dashboards'''

    def check_all(y):
        dashboards = sdk.all_dashboards(fields='id')
        dashboard_ids = [dashboard.id for dashboard in dashboards]
        print(len(dashboard_ids))

        for id in dashboard_ids:
            single_check(id, file=True)

        result_list_links.controls.append(ft.Text('DONE!'))
        page.update()

    button_for_all_dashboards_in_looker = ft.ElevatedButton(text='Check all Dashboards we have', height=50, on_click=check_all)

    '''First page'''

    def clean_list(x):
        result_list_links.controls = []
        page.update()

    clean_button = ft.ElevatedButton(text='Clean List', height=50, on_click=clean_list)
    dashboard_check = ft.Column(
        [
            ft.Row(
                [user_data, button_for_single_dash]
            ),
            ft.Row(
                [button_for_file, clean_button, button_for_all_dashboards_in_looker]
            ),
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
