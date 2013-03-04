"""autogenerated by genpy from jaco_arm/JacoPosition.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct


class JacoPosition(genpy.Message):
  _md5sum = "bb097489c67114a0031f0cb1cb64c70c"
  _type = "jaco_arm/JacoPosition"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """#Service used to send xyz position and xyz orientation values to the jaco arm

#x position in meters
float64 x_position

#y position in meters
float64 y_position

#z position in meters
float64 z_position

#x rotation
float64 x_rotation

#y rotation
float64 y_rotation

#z rotation
float64 z_rotation
"""
  __slots__ = ['x_position','y_position','z_position','x_rotation','y_rotation','z_rotation']
  _slot_types = ['float64','float64','float64','float64','float64','float64']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.

    The available fields are:
       x_position,y_position,z_position,x_rotation,y_rotation,z_rotation

    :param args: complete set of field values, in .msg order
    :param kwds: use keyword arguments corresponding to message field names
    to set specific fields.
    """
    if args or kwds:
      super(JacoPosition, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.x_position is None:
        self.x_position = 0.
      if self.y_position is None:
        self.y_position = 0.
      if self.z_position is None:
        self.z_position = 0.
      if self.x_rotation is None:
        self.x_rotation = 0.
      if self.y_rotation is None:
        self.y_rotation = 0.
      if self.z_rotation is None:
        self.z_rotation = 0.
    else:
      self.x_position = 0.
      self.y_position = 0.
      self.z_position = 0.
      self.x_rotation = 0.
      self.y_rotation = 0.
      self.z_rotation = 0.

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    :param buff: buffer, ``StringIO``
    """
    try:
      _x = self
      buff.write(_struct_6d.pack(_x.x_position, _x.y_position, _x.z_position, _x.x_rotation, _x.y_rotation, _x.z_rotation))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    :param str: byte array of serialized message, ``str``
    """
    try:
      end = 0
      _x = self
      start = end
      end += 48
      (_x.x_position, _x.y_position, _x.z_position, _x.x_rotation, _x.y_rotation, _x.z_rotation,) = _struct_6d.unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    :param buff: buffer, ``StringIO``
    :param numpy: numpy python module
    """
    try:
      _x = self
      buff.write(_struct_6d.pack(_x.x_position, _x.y_position, _x.z_position, _x.x_rotation, _x.y_rotation, _x.z_rotation))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    :param str: byte array of serialized message, ``str``
    :param numpy: numpy python module
    """
    try:
      end = 0
      _x = self
      start = end
      end += 48
      (_x.x_position, _x.y_position, _x.z_position, _x.x_rotation, _x.y_rotation, _x.z_rotation,) = _struct_6d.unpack(str[start:end])
      return self
    except struct.error as e:
      raise genpy.DeserializationError(e) #most likely buffer underfill

_struct_I = genpy.struct_I
_struct_6d = struct.Struct("<6d")
