# Quake Live Server Settings

## Updater script

Using updater script is easy. Point it to single or multiple access and workshop files and let it do the magic:

For example, if you have your access files in: `~/.quakelive/pub1/baseq3/access.txt` and
`~/.quakelive/priv1/baseq3/access.txt`, run the script with parameter:

`--access ~/.quakelive/pub1/baseq3/access.txt ~/.quakelive/priv1/baseq3/access.txt`

It will parse both access files, check for missing SteamID and add them. If You add additional parameter `--remove`
it will also remove and update existing roles. Otherwise the script will just point out possible change, line number
and ask you to update the file manually.

Workshop parser works almost the same way, except for that it only adds new ids, without removing or changing the
existing ones:

`--workshop ~/.quakelive/pub1/baseq3/workshop.txt ~/.quakelive/priv1/baseq3/workshop.txt`

You can use all 3 arguments: `--access`, `--workshop` and `--remove` at the same time