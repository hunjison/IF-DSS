#!/usr/bin/env python3

import os
import click
from art import text2art
from src.parse import parse_url
from src.ipmap import create_map
from src.track import node_track
from src.dnslink import dnslink_query
from src.reassemble import reassemble_chunks

def get_default_output():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(current_directory, "output")
    os.makedirs(output_directory, exist_ok=True)
    return output_directory

@click.group()
def cli():
    """IF-DSS: forensic Investigation Framework for Decentralized Storage System
    Code examples for case studies related to IPFS with Filecoin"""
    pass

@cli.command()
@click.argument('file_path')
@click.option('-o', '--output', default=get_default_output, help='Output path')
def parse(file_path, output):
    """Command to perform parsing"""
    click.echo(f'Parsing file: {file_path}')
    click.echo(f'Output path: {output}')

    parse_url(file_path, output)

@cli.command()
@click.argument('file_path')
@click.option('-o', '--output', default=get_default_output, help='Output path')
def ipmap(file_path, output):
    """Command to perform parsing"""
    click.echo(f'Parsing file: {file_path}')
    click.echo(f'Output path: {output}')

    create_map(file_path, output)

@cli.command()
@click.argument('file_path')
@click.option('--ipfs', required=True, help='IPFS path')
@click.option('-o', '--output', default=get_default_output, help='Output path')
def track(file_path, ipfs, output):
    """Command to perform tracking"""
    click.echo(f'Tracking file: {file_path}')
    click.echo(f'Command ipfs path: {ipfs}')
    click.echo(f'Output path: {output}')

    node_track(file_path, ipfs, output)

@cli.command()
@click.argument('file_path')
@click.option('-d', '--dig', default='dig', help='dig path')
@click.option('-o', '--output', default=get_default_output, help='Output path')
def trackdns(file_path, dig, output):
    """Command to perform DNS operation"""
    click.echo(f'Track DNS operation on file: {file_path}')
    click.echo(f'Command `dig` path: {dig}')
    click.echo(f'Output path: {output}')

    dnslink_query(file_path, dig, output)
    

@cli.command()
@click.argument('directory_path')
@click.option('-o', '--output', default=get_default_output, help='Output path')
def reassemble(directory_path, output):
    """Command to perform reassembly"""
    click.echo(f'Reassembling directory: {directory_path}')
    click.echo(f'Output path: {output}')
    
    reassemble_chunks(directory_path, output)

if __name__ == '__main__':
    print(text2art("IF-DSS"))
    cli()
