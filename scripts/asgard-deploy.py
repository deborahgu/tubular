#!/usr/bin/env python
import sys
import logging
import traceback
import click
import yaml
from os import path

# Add top-level module path to sys.path before importing tubular code.
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from tubular import asgard


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@click.command()
@click.option('--ami_id', envvar='AMI_ID', help='The ami-id to deploy')
@click.option('--out_file', help='output file for the deploy information yaml', default=None)
@click.option('--config-file', envvar='CONFIG_FILE', help='The config file to to get the ami_id from.')
@click.option('--dry-run', envvar='DRY_RUN', help='Don\'t actually deploy.', is_flag=True, default=False)
def deploy(ami_id, out_file, config_file, dry_run):
    if config_file:
        config = yaml.safe_load(open(config_file, 'r'))
    if not ami_id:
        if 'ami_id' in config:
            ami_id = config['ami_id']
        else:
            click.secho('AMI ID not specified in environment, on cli or in config file.', fg='red')
            sys.exit(1)

    ami_id = ami_id.strip()
    try:
        if not dry_run:
            deploy_info = asgard.deploy(ami_id)
        else:
            click.echo('Would have triggered a deploy of {}'.format(ami_id))
            deploy_info = {}

        if out_file:
            with open(out_file, 'w') as stream:
                yaml.safe_dump(deploy_info, stream, default_flow_style=False, explicit_start=True)
        else:
            print yaml.safe_dump(deploy_info, default_flow_style=False, explicit_start=True)

    except Exception as e:
        traceback.print_exc()
        click.secho('Error Deploying AMI: {0}.\nMessage: {1}'.format(ami_id, e.message), fg='red')
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    deploy()
