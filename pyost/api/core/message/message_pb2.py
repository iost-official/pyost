# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: core/message/message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='core/message/message.proto',
  package='message',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1a\x63ore/message/message.proto\x12\x07message\")\n\tBlockInfo\x12\x0e\n\x06number\x18\x01 \x01(\x03\x12\x0c\n\x04hash\x18\x02 \x01(\x0c\"K\n\x0e\x42lockHashQuery\x12\x0f\n\x07reqType\x18\x01 \x01(\x05\x12\r\n\x05start\x18\x02 \x01(\x03\x12\x0b\n\x03\x65nd\x18\x03 \x01(\x03\x12\x0c\n\x04nums\x18\x04 \x03(\x03\";\n\x11\x42lockHashResponse\x12&\n\nblockInfos\x18\x01 \x03(\x0b\x32\x12.message.BlockInfo\"*\n\nSyncHeight\x12\x0e\n\x06height\x18\x01 \x01(\x03\x12\x0c\n\x04time\x18\x02 \x01(\x03\x62\x06proto3')
)




_BLOCKINFO = _descriptor.Descriptor(
  name='BlockInfo',
  full_name='message.BlockInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='number', full_name='message.BlockInfo.number', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='hash', full_name='message.BlockInfo.hash', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=80,
)


_BLOCKHASHQUERY = _descriptor.Descriptor(
  name='BlockHashQuery',
  full_name='message.BlockHashQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='reqType', full_name='message.BlockHashQuery.reqType', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='message.BlockHashQuery.start', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='message.BlockHashQuery.end', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nums', full_name='message.BlockHashQuery.nums', index=3,
      number=4, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=82,
  serialized_end=157,
)


_BLOCKHASHRESPONSE = _descriptor.Descriptor(
  name='BlockHashResponse',
  full_name='message.BlockHashResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blockInfos', full_name='message.BlockHashResponse.blockInfos', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=218,
)


_SYNCHEIGHT = _descriptor.Descriptor(
  name='SyncHeight',
  full_name='message.SyncHeight',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='height', full_name='message.SyncHeight.height', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='message.SyncHeight.time', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=220,
  serialized_end=262,
)

_BLOCKHASHRESPONSE.fields_by_name['blockInfos'].message_type = _BLOCKINFO
DESCRIPTOR.message_types_by_name['BlockInfo'] = _BLOCKINFO
DESCRIPTOR.message_types_by_name['BlockHashQuery'] = _BLOCKHASHQUERY
DESCRIPTOR.message_types_by_name['BlockHashResponse'] = _BLOCKHASHRESPONSE
DESCRIPTOR.message_types_by_name['SyncHeight'] = _SYNCHEIGHT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BlockInfo = _reflection.GeneratedProtocolMessageType('BlockInfo', (_message.Message,), dict(
  DESCRIPTOR = _BLOCKINFO,
  __module__ = 'core.message.message_pb2'
  # @@protoc_insertion_point(class_scope:message.BlockInfo)
  ))
_sym_db.RegisterMessage(BlockInfo)

BlockHashQuery = _reflection.GeneratedProtocolMessageType('BlockHashQuery', (_message.Message,), dict(
  DESCRIPTOR = _BLOCKHASHQUERY,
  __module__ = 'core.message.message_pb2'
  # @@protoc_insertion_point(class_scope:message.BlockHashQuery)
  ))
_sym_db.RegisterMessage(BlockHashQuery)

BlockHashResponse = _reflection.GeneratedProtocolMessageType('BlockHashResponse', (_message.Message,), dict(
  DESCRIPTOR = _BLOCKHASHRESPONSE,
  __module__ = 'core.message.message_pb2'
  # @@protoc_insertion_point(class_scope:message.BlockHashResponse)
  ))
_sym_db.RegisterMessage(BlockHashResponse)

SyncHeight = _reflection.GeneratedProtocolMessageType('SyncHeight', (_message.Message,), dict(
  DESCRIPTOR = _SYNCHEIGHT,
  __module__ = 'core.message.message_pb2'
  # @@protoc_insertion_point(class_scope:message.SyncHeight)
  ))
_sym_db.RegisterMessage(SyncHeight)


# @@protoc_insertion_point(module_scope)
