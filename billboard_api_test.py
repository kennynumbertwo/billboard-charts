import billboard
import json
import pandas as pd
import pandas.io.formats.excel
import xlsxwriter
from song_album_lists import all_us_albums, all_us_songs, chart_lists


def get_chart(chart, date):
    chart_info = billboard.ChartData(chart, date=date)
    return chart_info


def get_year_end_chart(chart, year):
    chart_info = billboard.ChartData(chart, year=year)
    return chart_info


def convert_string_json(chart):
    converted_json = json.loads(chart)
    return converted_json


# Start and end dates for the report. Each must be a Saturday
dates = ['2022-03-19', '2022-03-26', '2022-04-02', '2022-04-09']
start_date = "2022-03-19"
end_date = "2022-04-09"
program_running = True

# Lists for printing in terminal
peer_titles_matched = ['Date, Chart Name, This Week, Last Week, WOC, High Pos, Song/Album, Artist']
new_song_entries = ['Date, Chart Name, This Week, Last Week, Song, Artist']
new_album_entries = ['Date, Chart Name, This Week, Last Week, Album, Artist']

# Lists for pandas dataframe peer chart positions
pd_date = []
pd_chart_name = []
pd_this_week = []
pd_last_week = []
pd_woc = []
pd_high_pos = []
pd_title = []
pd_artist = []

# Lists for pandas dataframe new entries
pd_ne_date = []
pd_ne_chart_name = []
pd_ne_this_week = []
pd_ne_last_week = []
pd_ne_title = []
pd_ne_artist = []

for chart_date in dates:
# while program_running is True:
    for chart in chart_lists.pop_country_song_charts:
        song_chart = get_chart(chart, chart_date).json()
        song_chart_json = convert_string_json(song_chart)
        save_file = 'chart_files/single_charts.json'
        with open(save_file, 'w') as f:
            json.dump(song_chart_json, f, indent=4)
        load_file = 'chart_files/single_charts.json'
        with open(load_file) as f:
            json_chart_info = json.load(f)
        all_charting_songs = json_chart_info['entries']
        date = json_chart_info['date']
        date_time = pd.to_datetime(date)
        chart_name = json_chart_info['title']
        for entry in all_charting_songs:
            entry_dicts = entry
            artist = entry_dicts['artist']
            title = entry_dicts['title']
            this_week = entry_dicts['rank']
            last_week = entry_dicts['lastPos']
            woc = entry_dicts['weeks']
            high_pos = entry_dicts['peakPos']
            # Creates a printable version for the terminal
            all_entries_formatted = [
                f"{date}, {chart_name}, {this_week}, {last_week}, {woc}, {high_pos}, {title}, {artist}"]
            new_entries_formatted= [
                f"{date}, {chart_name}, {this_week}, New Entry, {title}, {artist}"]
            for song in all_entries_formatted:
                # Song list changed here
                if title.lower() in all_us_songs.pop_country_songs:
                    peer_titles_matched.append(song)
                    # Create lists for the pandas dataframe
                    pd_date.append(date_time.strftime('%m/%d/%Y'))
                    pd_chart_name.append(chart_name)
                    pd_this_week.append(this_week)
                    pd_last_week.append(last_week)
                    pd_woc.append(woc)
                    pd_high_pos.append(high_pos)
                    pd_title.append(title)
                    pd_artist.append(artist)
            for song in new_entries_formatted:
                if entry_dicts['isNew'] is True:
                    new_song_entries.append(song)
                    pd_ne_date.append(date_time.strftime('%m/%d/%Y'))
                    pd_ne_chart_name.append(chart_name)
                    pd_ne_this_week.append(this_week)
                    pd_ne_last_week.append('NE')
                    pd_ne_title.append(title)
                    pd_ne_artist.append(artist)
    for chart in chart_lists.pop_country_albums_charts:
        album_chart = get_chart(chart, chart_date).json()
        album_chart_json = convert_string_json(album_chart)
        save_file = 'chart_files/album_charts.json'
        with open(save_file, 'w') as f:
            json.dump(album_chart_json, f, indent=4)
        load_file = 'chart_files/album_charts.json'
        with open(load_file) as f:
            json_chart_info = json.load(f)
        all_charting_albums = json_chart_info['entries']
        date = json_chart_info['date']
        date_time = pd.to_datetime(date)
        chart_name = json_chart_info['title']
        for entry in all_charting_albums:
            entry_dicts = entry
            artist = entry_dicts['artist']
            title = entry_dicts['title']
            this_week = entry_dicts['rank']
            last_week = entry_dicts['lastPos']
            if last_week == 0:
                last_week = 'RE'
            woc = entry_dicts['weeks']
            high_pos = entry_dicts['peakPos']
            all_entries_formatted = [
                f"{date}, {chart_name}, {this_week}, {last_week}, {woc}, {high_pos}, {title}, {artist}"]
            new_entries_formatted= [
                f"{date}, {chart_name}, {this_week}, New Entry, {title}, {artist}"]
            for album in all_entries_formatted:
                # Album list changed here
                if title.lower() in all_us_albums.pop_country_albums:
                    peer_titles_matched.append(album)
                    pd_date.append(date_time.strftime('%m/%d/%Y'))
                    pd_chart_name.append(chart_name)
                    pd_this_week.append(this_week)
                    pd_last_week.append(last_week)
                    pd_woc.append(woc)
                    pd_high_pos.append(high_pos)
                    pd_title.append(title)
                    pd_artist.append(artist)
                if title.lower() == "greatest hits":
                    if artist.lower() in all_us_albums.greatest_hits:
                        peer_titles_matched.append(album)
                        pd_date.append(date_time.strftime('%m/%d/%Y'))
                        pd_chart_name.append(chart_name)
                        pd_this_week.append(this_week)
                        pd_last_week.append(last_week)
                        pd_woc.append(woc)
                        pd_high_pos.append(high_pos)
                        pd_title.append(title)
                        pd_artist.append(artist)
            for album in new_entries_formatted:
                if entry_dicts['isNew'] is True:
                    new_album_entries.append(album)
                    pd_ne_date.append(date_time.strftime('%m/%d/%Y'))
                    pd_ne_chart_name.append(chart_name)
                    pd_ne_this_week.append(this_week)
                    pd_ne_last_week.append('NE')
                    pd_ne_title.append(title)
                    pd_ne_artist.append(artist)
    # uncomment if you want to run for the start date only
    # program_running = False
    # comment out if you want to run for the start date only
    # start_date = json_chart_info['nextDate']
    # if start_date == end_date:
    #     program_running = False
    # else:
    #     continue

print('\n')

for track in peer_titles_matched:
    print(track)

print('\n')

for song in new_song_entries:
    print(song)

print('\n')

for album in new_album_entries:
    print(album)

# Create pandas dataframe from peermusic pd lists
pd_dataframe_peer_charts = {
    'Date': pd_date,
    'Chart Name': pd_chart_name,
    'TW': pd_this_week,
    'LW': pd_last_week,
    'WOC': pd_woc,
    'HP': pd_high_pos,
    'Song/Album': pd_title,
    'Artist': pd_artist
}

# Create pandas dataframe from new entries lists
pd_dataframe_new_entry_charts = {
    'Date': pd_ne_date,
    'Chart Name': pd_ne_chart_name,
    'TW': pd_ne_this_week,
    'LW': pd_ne_last_week,
    'Song/Album': pd_ne_title,
    'Artist': pd_ne_artist
}

# Create an pandas Excel Writer object and pass the engine argument for formatting purposes
writer = pd.ExcelWriter(f'./Reports/International_Report_{start_date}.xlsx', engine="xlsxwriter")

df = pd.DataFrame(pd_dataframe_peer_charts)
df_ne = pd.DataFrame(pd_dataframe_new_entry_charts)
df.to_excel(writer, sheet_name='US Chart Positions', index=False)
df_ne.to_excel(writer, sheet_name='New Entries', index=False)

workbook = writer.book

# Variable for peer chart worksheet
worksheet = writer.sheets['US Chart Positions']

# Set formatting for excel spreadsheets
data_format = workbook.add_format({'font_name': 'Calibri', 'font_size': 10})
data_position_format = workbook.add_format({'font_name': 'Calibri', 'font_size': 10, 'align': 'right'})
header_format = workbook.add_format({'bg_color': '#e0e0e0', 'border': True, 'border_color': '#b7b7b7', 'font_size': 10})
worksheet.set_column('A:A', 14, data_format)
worksheet.set_column('B:B', 18, data_format)
worksheet.set_column('C:F', 8, data_position_format)
worksheet.set_column('G:G', 50, data_format)
worksheet.set_column('H:H', 56, data_format)

(max_row, max_col) = df.shape
# List for creating my own custom headers for formatting purposes
headers = ['Date', 'Chart Name', 'TW', 'LW', 'WOC', 'HP', 'Song/Album', 'Artist']
header_start = 0
for header in headers:
    worksheet.write(0, header_start, header, header_format)
    header_start += 1
worksheet.autofilter(0, 0, max_row, max_col - 1)

# Variable for new entries chart worksheet
worksheet_ne = writer.sheets['New Entries']

# Set formatting for excel spreadsheet
header_format_ne = workbook.add_format({'bg_color': '#e0e0e0', 'border': True, 'border_color': '#b7b7b7', 'font_size': 10})
worksheet_ne.set_column('A:A', 14, data_format)
worksheet_ne.set_column('B:B', 18, data_format)
worksheet_ne.set_column('C:D', 8, data_position_format)
worksheet_ne.set_column('E:E', 50, data_format)
worksheet_ne.set_column('F:F', 56, data_format)

(max_row, max_col) = df_ne.shape
# List for creating my own custom headers for formatting purposes
headers_ne = ['Date', 'Chart Name', 'TW', 'LW', 'Song/Album', 'Artist']
header_start_ne = 0
for header in headers_ne:
    worksheet_ne.write(0, header_start_ne, header, header_format_ne)
    header_start_ne += 1
worksheet_ne.autofilter(0, 0, max_row, max_col - 1)


# Save the file
writer.save()
