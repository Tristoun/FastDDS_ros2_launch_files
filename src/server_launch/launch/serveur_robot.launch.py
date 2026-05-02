from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
import os
from ament_index_python.packages import get_package_share_directory
import yaml

def generate_launch_description() :
    
    package_dir = get_package_share_directory('server_launch')
    config_path = os.path.join(package_dir, 'config', 'params.yaml')

    with open(config_path, 'r') as param:
        config_data = yaml.safe_load(param)

    #On load l'ip serveur
    try :
        ip_port = f'{config_data["network_config"]["ip"]}:{config_data["network_config"]["port"]}'
    except KeyError :
        print("Issue with getting params : set 127.0.0.1 default")
        ip_port = "127.0.0.1:11811"

    #Utilisation de fast dds
    set_fast_dds = SetEnvironmentVariable(
        name="RMW_IMPLEMENTATION", value='rmw_fastrtps_cpp'
    )

    #config serveur
    set_server = SetEnvironmentVariable(
        name='ROS_DISCOVERY_SERVER', value=ip_port
    )

    start_server = ExecuteProcess(
        cmd=['fastdds', 'discovery', '--server-id', '0'],
        shell=True,
        output='screen'
    )
    
    return LaunchDescription ([
        set_fast_dds,
        set_server,
        start_server
    ])