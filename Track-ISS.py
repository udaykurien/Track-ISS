# Import modules
import requests, json, time, argparse
import plotly.express as px

# Define arguments
parser=argparse.ArgumentParser(description='Track and graph ISS position.')
parser.add_argument('-d','--duration',type=int,metavar='',
                    help='Total tracking duration.')
parser.add_argument('-s','--sample_freq',type=int,metavar='',
                    help='Interval between ISS location retrieval')
parser.add_argument('-p','--projection',type=str,metavar='',
                   help='Projection type of map.')
parser.add_argument('-f','--file',type=str,metavar='',
                   help='File name to save data to.')
parser.add_argument('-a','--animation',type=int,metavar='',
                   help='Animated plot.')
args=parser.parse_args()

# Alias arguments
t_total=args.duration
t_interval=args.sample_freq
projection_mode=args.projection
f_name=args.file
animations=args.animation

# File IO
def file_io(mode,f_name,json_data=None):
    if mode == 'a+':
        with open(f_name,mode) as f_handler:
            json.dump(json_data,f_handler)
            f_handler.write("\n")
    elif mode == 'r' :
        with open(f_name,mode) as f_handler:
            f_content = f_handler.readlines()
            return f_content

# Get data from ISS and store in file
def get_iss_info(f_name='default',write_optn='n',t_interval=1,t_total=1):
    print("Total number of data points: {}".format(int(t_total/t_interval)))
    url='http://api.open-notify.org/iss-now.json'
    t_counter = 0
    t_now = 1
    info_lst = []
    while t_now <= t_total:
        iss_data = requests.get(url).json()
        t_now += t_interval
        t_counter += 1
        if write_optn == 'y':
            mode = 'a+'
            file_io(mode,f_name,iss_data)
            print("Data points: {}, Run time: {}s".format(t_counter,t_now))
        else :
            print(iss_data)
        time.sleep(t_interval)
    return 0

# Main program
# Record ISS location
get_iss_info(f_name,'y',t_interval,t_total)
print("Data collection complete.")
# Read saved data
f_content = file_io('r',f_name)
# Extract ISS location data into lists
iss_data_lst = []
lat_lst = []
lon_lst = []
time_lst = []
for line in f_content:
    iss_data_lst.append(json.loads(line.strip()))
time_zero = iss_data_lst[0]['timestamp']
for element in iss_data_lst:
    lat_lst.append(element['iss_position']['latitude'])
    lon_lst.append(element['iss_position']['longitude'])
    time_lst.append((element['timestamp']-time_zero)/60)
# Make graphs
if animations == 0:
    anime_val=None
elif animations == 1:
    anime_val = time_lst
fig = px.scatter_geo(lat=lat_lst,lon=lon_lst,projection=projection_mode,
                      opacity=0.8,hover_name=time_lst,animation_frame=anime_val)
fig.show()