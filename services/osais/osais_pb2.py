# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: osais.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bosais.proto\x12\x05osais\"&\n\x05Query\x12\r\n\x05query\x18\x01 \x01(\t\x12\x0e\n\x06worker\x18\x02 \x01(\t\"\x18\n\x06\x41nswer\x12\x0e\n\x06\x61nswer\x18\x01 \x01(\t22\n\tpostOSAIS\x12%\n\x04\x63\x61ll\x12\x0c.osais.Query\x1a\r.osais.Answer\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osais_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_QUERY']._serialized_start=22
  _globals['_QUERY']._serialized_end=60
  _globals['_ANSWER']._serialized_start=62
  _globals['_ANSWER']._serialized_end=86
  _globals['_POSTOSAIS']._serialized_start=88
  _globals['_POSTOSAIS']._serialized_end=138
# @@protoc_insertion_point(module_scope)
