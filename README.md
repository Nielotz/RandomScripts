# RandomScripts
 
### TVSeriesOrderFixer - rename and move season episodes to fix order.
Uses season to organize in folders.

Setup:<br>
`SERIES_FOLDER_PATH = r"D:\Futurama"  # Path to folder with seasons folder.`<br>
`SERIES_NAME = "FUTURAMA"  # Used to createname filenames.`<br>
Organize episode episodes_data_from_explorer.key by using episode_data[global_episode_id]<br>
`episode_data = {global_episode_id: EpisodeData(end_id, season_id, season_episode_id, title), }`
`episodes_data_from_explorer = {existing_filename : global_episode_id}`<br>
You need to change 
`season_padded: str = old_episode_filename.split(".")[1].split("E")[0].upper()` to receive Seasonx folder name<br><br>
Series folder structure:<br>
MainCatalog<br>
|--Seasonx<br>
|--Seasony<br>
|--Seasonz<br>


![](TVSeriesOrderFixer.png)