class Address:
    def __init__(self, addressID=None, addressName=None, tel =None ,default=None, province=None, city=None, area=None, description=None, post=None, zipCode=None):
        self._addressID = addressID
        self._addressName = addressName
        self._default = default
        self._tel = tel
        self._province = province
        self._city = city
        self._area = area
        self._description = description
        self._post = post
        self._zipCode = zipCode

    def getAddressID(self):
        return self._addressID

    def setAddressID(self, addressID):
        self._addressID = addressID

    def getAddressName(self):
         return self._addressName

    def setAddressName(self, addressName):
        self.addressName = addressName

    def isDefault(self):
        return self._default

    def setDefault(self, default):
        self._default = default

    def getTel(self):
        return self._tel

    def setTel(self,tel):
        self._tel = tel


    def getProvince(self):
        return self._province

    def setProvince(self, province):
        self._province = province

    def getCity(self):
        return self._city

    def setCity(self, city):
        self._city = city

    def getArea(self):
        return self._area

    def setArea(self, area):
        self._area = area

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getPost(self):
        return self._post

    def setPost(self, post):
        self._post = post

    def getZipCode(self):
        return self._zipCode

    def setZipCode(self, zipCode):
        self._zipCode = zipCode
