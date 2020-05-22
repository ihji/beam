"""Integration test for Python cross-language pipelines for Java KafkaIO."""

from __future__ import absolute_import

import contextlib
import os
import socket
import subprocess
import time
import typing
import unittest

from nose.plugins.attrib import attr
import grpc

import apache_beam as beam
from apache_beam.io.external.kafka import ReadFromKafka
from apache_beam.io.external.kafka import WriteToKafka
from apache_beam.metrics import Metrics
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.testing.test_pipeline import TestPipeline


class CrossLanguageKafkaIO(object):

  def __init__(self, bootstrap_servers, topic, expansion_service=None):
    self.bootstrap_servers = bootstrap_servers
    self.topic = topic
    self.expansion_service = expansion_service or (
        'localhost:%s' % os.environ.get('EXPANSION_PORT'))
    self.sum_counter = Metrics.counter('source', 'elements_sum')

  def build_pipeline(self, pipeline):
    _ = (
        pipeline
        | 'Impulse' >> beam.Impulse()
        | 'Generate' >> beam.FlatMap(lambda x: range(1000))
        | 'Reshuffle' >> beam.Reshuffle()
        | 'MakeKV' >> beam.Map(lambda x:
                               (b'', str(x).encode())).with_output_types(
      typing.Tuple[bytes, bytes])
        | 'WriteToKafka' >> WriteToKafka(
      producer_config={'bootstrap.servers': self.bootstrap_servers},
      topic=self.topic,
      expansion_service=self.expansion_service))
    _ = (
        pipeline
        | 'ReadFromKafka' >> ReadFromKafka(
      consumer_config={
        'bootstrap.servers': self.bootstrap_servers,
        'auto.offset.reset': 'earliest'
      },
      topics=[self.topic],
      expansion_service=self.expansion_service)
        | 'Windowing' >> beam.WindowInto(
      beam.window.FixedWindows(300),
      trigger=beam.transforms.trigger.AfterProcessingTime(60),
      accumulation_mode=beam.transforms.trigger.AccumulationMode
        .DISCARDING)
        | 'DecodingValue' >> beam.Map(lambda elem: int(elem[1].decode()))
        | 'CombineGlobally' >> beam.CombineGlobally(sum).without_defaults()
        | 'SetSumCounter' >> beam.Map(self.sum_counter.inc))

  def run_xlang_kafkaio(self, pipeline):
    self.build_pipeline(pipeline)
    pipeline.run(False)


@attr('UsesCrossLanguageTransforms')
@unittest.skipUnless(
  os.environ.get('LOCAL_KAFKA_JAR'),
  "LOCAL_KAFKA_JAR environment var is not provided.")
@unittest.skipUnless(
  os.environ.get('EXPANSION_JAR'),
  "EXPANSION_JAR environment var is not provided.")
class CrossLanguageKafkaIOTest(unittest.TestCase):
  def get_open_port(self):
    s = None
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:  # pylint: disable=bare-except
      # Above call will fail for nodes that only support IPv6.
      s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

  @contextlib.contextmanager
  def local_services(self, expansion_service_jar_file, local_kafka_jar_file):
    expansion_service_port = str(self.get_open_port())
    kafka_port = str(self.get_open_port())
    zookeeper_port = str(self.get_open_port())

    expansion_server = None
    kafka_server = None
    try:
      expansion_server = subprocess.Popen([
        'java', '-jar', expansion_service_jar_file,
        expansion_service_port
      ])
      kafka_server = subprocess.Popen([
        'java', '-jar', local_kafka_jar_file,
        kafka_port, zookeeper_port
      ])
      time.sleep(3)
      channel_creds = grpc.local_channel_credentials()
      with grpc.secure_channel('localhost:%s' % expansion_service_port,
                               channel_creds) as channel:
        grpc.channel_ready_future(channel).result()

      yield expansion_service_port, kafka_port
    finally:
      if expansion_server:
        expansion_server.kill()
      if kafka_server:
        kafka_server.kill()

  def get_options(self):
    options = PipelineOptions([
      '--runner', 'FlinkRunner',
      '--parallelism', '2',
      '--experiment', 'beam_fn_api'
    ])
    return options

  def test_kafkaio_write_read(self):
    local_kafka_jar = os.environ.get('LOCAL_KAFKA_JAR')
    expansion_service_jar = os.environ.get('EXPANSION_JAR')
    with self.local_services(expansion_service_jar, local_kafka_jar) as (expansion_port, kafka_port):
      options = self.get_options()
      p = TestPipeline(options=options)
      CrossLanguageKafkaIO(
          'localhost:%s' % kafka_port, 'localhost:%s' % expansion_port
      ).build_pipeline(p)
      job = p.run()
      job.wait_until_finish(180000)
      job.cancel()