# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: sistem_kasir.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'sistem_kasir.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12sistem_kasir.proto\"\xf9\x01\n\x0bTransaction\x12\x10\n\x08retailer\x18\x01 \x01(\t\x12\x13\n\x0bretailer_id\x18\x02 \x01(\x05\x12\x14\n\x0cinvoice_date\x18\x03 \x01(\t\x12\x0e\n\x06region\x18\x04 \x01(\t\x12\r\n\x05state\x18\x05 \x01(\t\x12\x0c\n\x04\x63ity\x18\x06 \x01(\t\x12\x0f\n\x07product\x18\x07 \x01(\t\x12\x16\n\x0eprice_per_unit\x18\x08 \x01(\x01\x12\x12\n\nunits_sold\x18\t \x01(\x05\x12\x13\n\x0btotal_sales\x18\n \x01(\x01\x12\x18\n\x10operating_profit\x18\x0b \x01(\x01\x12\x14\n\x0csales_method\x18\x0c \x01(\t\"3\n\x0cStockRequest\x12\x0f\n\x07product\x18\x01 \x01(\t\x12\x12\n\nunits_sold\x18\x02 \x01(\x05\"\x1d\n\rReportRequest\x12\x0c\n\x04type\x18\x01 \x01(\t\"\x19\n\x06Report\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"+\n\x08Response\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t27\n\x08\x46rontend\x12+\n\x10InputTransaction\x12\x0c.Transaction\x1a\t.Response28\n\x07\x42\x61\x63kend\x12-\n\x12ProcessTransaction\x12\x0c.Transaction\x1a\t.Response25\n\nStokBarang\x12\'\n\x0bUpdateStock\x12\r.StockRequest\x1a\t.Response26\n\tReporting\x12)\n\x0eGenerateReport\x12\x0e.ReportRequest\x1a\x07.Reportb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sistem_kasir_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRANSACTION']._serialized_start=23
  _globals['_TRANSACTION']._serialized_end=272
  _globals['_STOCKREQUEST']._serialized_start=274
  _globals['_STOCKREQUEST']._serialized_end=325
  _globals['_REPORTREQUEST']._serialized_start=327
  _globals['_REPORTREQUEST']._serialized_end=356
  _globals['_REPORT']._serialized_start=358
  _globals['_REPORT']._serialized_end=383
  _globals['_RESPONSE']._serialized_start=385
  _globals['_RESPONSE']._serialized_end=428
  _globals['_FRONTEND']._serialized_start=430
  _globals['_FRONTEND']._serialized_end=485
  _globals['_BACKEND']._serialized_start=487
  _globals['_BACKEND']._serialized_end=543
  _globals['_STOKBARANG']._serialized_start=545
  _globals['_STOKBARANG']._serialized_end=598
  _globals['_REPORTING']._serialized_start=600
  _globals['_REPORTING']._serialized_end=654
# @@protoc_insertion_point(module_scope)
