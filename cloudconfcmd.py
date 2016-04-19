import json
import jinja2
import logging
import argparse


def get_servers_data(datafile):
    with open(datafile) as json_file:
        json_data = json.load(json_file)
    return json_data


def import_cloud_template(cloudtemplatefile):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(cloudtemplatefile)
#    with open(cloudtemplatefile) as template_file:
#        t = templateEnv.get_template(template_file)
    return template


def put_servers_data(json_data, datafile):
    with open(datafile, 'w') as fp:
        json.dump(json_data, fp, sort_keys=True, indent=4)


def render_cloudfile(server_name, servers_data, cloudtemplatefile, template):
    worker_name = server_name
    worker_ip = servers_data['servers'][server_name]['worker_ip']
    etcd_endpoint = servers_data['etcd']['etcd_endpoint']
    logging.debug('list of templateVars:')
    logging.debug('worker: %s, ip: %s, etcd: %s' % (worker_name,
                                                    worker_ip,
                                                    etcd_endpoint))
    templateVars = {"worker_name": worker_name,
                    "worker_ip": worker_ip,
                    "etcd_endpoint": etcd_endpoint}
    outputText = template.render(templateVars)
    print outputText
    return


def put_cloud_file():
    return


parser = argparse.ArgumentParser(description='CloudConfig generator')
parser.add_argument('-s', '--server',
                    help='server name', required=True)
parser.add_argument('-d', '--debug',
                    help='debug value [DEBUG|Default=none]', required=False)
args = parser.parse_args()

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
if args.debug:
    logger.setLevel(args.debug)

logging.debug('Debug on')

datafile = 'servermap.json'
outdatafile = 'datafile.json'
cloudtemplatefile = 'workerTEMPLATE.yaml'

servers_data = get_servers_data(datafile)
cloud_template = import_cloud_template(cloudtemplatefile)
render_cloudfile(args.server, servers_data, cloudtemplatefile, cloud_template)
logging.debug('servers_data: %s' % servers_data['servers'])

#
# put_servers_data(servers_data, outdatafile)
