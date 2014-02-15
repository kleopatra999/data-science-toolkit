import argparse
import os
import time
from . import run_server_from_args


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ami', dest='ami', type=str,
                        default="ami-d6e785e6",
                        help='The AMI to launch')
    parser.add_argument('--num-nodes', dest='node_count', type=int,
                        default=20,
                        help="Number of worker nodes to launch")
    parser.add_argument('--num-topics', dest='num_topics', type=int, action='store',
                        default=os.getenv('NUM_TOPICS', 999),
                        help="The number of topics for the model to use")
    parser.add_argument('--path-prefix', dest='path_prefix', type=str, action='store',
                        default=os.getenv('PATH_PREFIX', '/mnt/'),
                        help="Where to save the model")
    parser.add_argument('--max-topic-frequency', dest='max_topic_frequency', type=int,
                        default=os.getenv('MAX_TOPIC_FREQUENCY', 500),
                        help="Threshold for number of videos a given topic appears in")
    parser.add_argument('--model-prefix', dest='model_prefix', type=str,
                        default=os.getenv('MODEL_PREFIX', time.time()),
                        help="Prefix to uniqueify model")
    parser.add_argument('--s3-prefix', dest='s3_prefix', type=str,
                        default=os.getenv('S3_PREFIX', "models/wiki/"),
                        help="Prefix on s3 for model location")
    parser.add_argument('--auto-launch', dest='auto_launch', type=bool,
                        default=os.getenv('AUTOLAUNCH_NODES', True),
                        help="Whether to automatically launch distributed nodes")
    parser.add_argument('--instance-count', dest='instance_count', type=int,
                        default=os.getenv('NODE_INSTANCES', 20),
                        help="Number of node instances to launch")
    parser.add_argument('--node-ami', dest='node_ami', type=str,
                        default=os.getenv('NODE_AMI', "ami-d6e785e6"),
                        help="AMI of the node machines")
    parser.add_argument('--dont-terminate-on-complete', dest='terminate_on_complete', action='store_false',
                        default=os.getenv('TERMINATE_ON_COMPLETE', True),
                        help="Prevent terminating this instance")
    parser.add_argument('--master-ip', dest='master_ip', default='54.200.131.148',
                        help="The elastic IP address to associate with the master server")
    parser.add_argument('--killable', dest='killable', action='store_true', default=False,
                        help="Keyboard interrupt terminates master")
    return parser.parse_args()


def main():
    run_server_from_args(get_args(), 'wikia_dstk.lda.wiki_lda_server')


if __name__ == '__main__':
    main()