# (c) 2003 Nuxeo SARL <http://nuxeo.com>
# $Id$

# The storage adapters are classes used to abstract the action of setting and
# getting data for documents. With adapters some data could reside as attributes
# on the document, some could reside in an SQL database, some could be computed
# and some could reside in the file system.
#
# The adapter will assume that the data to be set or fetched is validated and of
# the correct type, so no check will be done in any direction.
#
# the get/set/has_key/del_key methods can be used directly, but are primarily
# for internal use by the StorageAdapter itself. This is because each call to these
# will create one call to storage, which would result in one SQL statement if the
# storage is an RDBM. Instead, in most cases, the readDataStructure() and
# writeDataStructure() would be used. These methods would consolidate all
# data into as few SQL calls as possible.
#
# The StorageAdapter is also responsible for mapping field ids into storage ids.
# The field id and storage id is mostly the same, but there could be instances
# where you want them to differ. One place could be mapping them into namespaces,
# the other instance would be when you have two SQL fields with the same name in
# different tables. They would have to have different field ids, but the same
# storage id.
#
# The adapter needs the following information when setting data:
# - Where the data is stored
# - Who: Which document this is about
# - Which data is to be fetched (ie the field name)
# - Whence: What name space does this belong to
# - What: For setting data, it also needs to have the data, of course.
#
# The name space (Whence) if any, will be an internal setting.
# 
# What to set is obviously external, and so is Which field name to use.
# Who (the document) is also external. These three must be passed to the method
# storing the data, for all adapters.
#
# For some adapters, such as an SQL adapter, the Where is an internal setting,
# while for others, like the property adapter, it will be external. Luckily in
# the property adapter case, it will be the document, and Who is alreaady passed.
# I'm trying to think of any other cases where Where is external, to figure out
# if that would be separate from the document in any case, because if it is, we
# would need to pass Where too. But I can't see that this is necessary.
# In the case of a file system adapter, the Where is the file name, and that would
# be a combination of a base setting in the adapter itself, and the physical path
# to the document, so yeat again the document being passed is enough.
#
# That leaves the interface as such:
#   def set(self, who, which, what)
#   def get(self, who, which)
#   def has(self, who, which)
#   def del(self, who, which)

from DataStructure import DataStructure

class BasicStorageAdapter:

    def __init__(self, document, fields, namespace=''):
        """Creates a StorageAdapter

        document is the NuxCPS3Document, namespace is a string,
        fields is a dict of fieldid's and fields.
        """
        self._document = document
        self._namespace = namespace
        self._fields = fields

    def getFieldStorageId(self, field_id):
        """This gets the physical id used for the fields storage"""
        field = self._fields[field_id]
        return field.getStorageId()

    def set(self, field_id, data):
        raise NotImplementedError

    def get(self, field_id):
        """Get data or none

        Raises an KeyError if field_id is not in _fields, and returns
        the default if the data does not exist in the storage (or the
        document is None), and the field is required, or None if it is
        not required
        """
        raise NotImplementedError

    def delete(self, field_id):
        raise NotImplementedError

    def has_data(self, field_id):
        return self.get(field_id) is not None

    def readData(self):
        """Returns a dict with all the data"""
        data = {}
        for fieldid in self._fields.keys():
            data[fieldid] = self.get(fieldid)
        return data

    def writeData(self, dict):
        """Updated the content of a storage from a dictionary"""
        for fieldid in dict.keys():
            data = dict[fieldid]
            if data is None and self.has_data(fieldid):
                self.delete(fieldid)
            else:
                self.set(fieldid, data)



class AttributeStorageAdapterFactory:
    """The AdapterFactory creates StorageAdapters

    The Factory contains all settings used by the StorageAdapters. The
    AttributeStorage uses no settings at all. And the Factory is therefore
    only one method: the factory method.
    """

    def makeStorageAdapter(self, document):
        return AttributeStorageAdapter(document)


