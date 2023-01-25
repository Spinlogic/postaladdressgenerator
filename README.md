# Postal Address Generator

Generates a file with random postal address of the region of Madrid.

I use this program to generate *csv files* with lots of random contacts. 
These files are used to measure the time that it takes to import large sets of contacts into
a state of the art **EMNS** (Emergency Mass Notification System) of the company that I work for.

You can adapt it anyway that fits your needs.

# Command line

```python
python .\main.py -g -c 50 -s 2  streets_file firstnames_file surnames_file output_file
```

Options:

| Parameter |                                       | 
|:---------:|---------------------------------------|
| -g        | Resolve geocoordinates of addresses   |
| -c        | Number of contacts to generate        |
| -s        | Number of surnames (default 1)        |
| streets_file | File with the list of streets formated as in ./data/ListaDeCallesDeMadrid.txt |
| firstnames_file | File with the list if firstnames as in ./data/ListaDeNombresPropios.txt |
| surnames_file | File with the list if surnames as in ./data/ListaDeApellidos.txt |
| outout_file | path and name for generated contacts file |

# Output file content

The output of this program is a **csv** file in which the first line is a header with the
names of the columns, and the rest of lines are contacts (one per line).

In the current version, each row has the following columns:

| Column               |                                                               |
|:--------------------:|---------------------------------------------------------------|
| firstnames           | First name of the contact                                     |
| surnames             | Surnames / family names of the contact                        |
| country_code         | ISO two letter country code (e.g. ES, UK)                     |
| prefix_number        | International dialing code for the country (e.g. +34, +1)     |
| number               | Phone number (as it would be dialed with international code)  |
| email                | Email address                                                 |
| locations1:line1     | Street and number                                             |
| locations1:city      | City / town                                                   |
| locations1:state     | State / province / prefecture / region name                   |
| locations1:country   | Country name or ISO two letter country code                   |
| locations1:latitude  | Latitude geo-coordinate for the location                      |
| locations1:longitude | Longitude geo-coordinate for the location                     |
| group:Fake           | The contact belongs to the Fake groups                        |

You can include more locations by using *location2:*, *location3:*, and so on.

You can also include as many groups as you want. I added *group:Fake* to identify 
these contacts in the system as *Fake* and remove them easily.

**Note:** Geolocation (lat, lon) is only included if the *-g* option is present in the 
command. If this option is added, then the program queries the location coordinates of 
the address for each contact, which takes time to resolve. I.e. including the *-g* 
severely <span style="color:#F05050">slows down</span> the execution.
