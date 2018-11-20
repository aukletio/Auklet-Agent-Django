import factory


class MonitoringDataGenerator(object):
    def __init__(self, data):
        self.commitHash = data[0]
        self.id = data[1]
        self.publicIP = data[2]
        self.timestamp = data[3]
        self.application = data[4]
        self.macAddressHash = data[5]

        self.lineNumber = data[6]
        self.nSamples = data[7]
        self.functionName = data[8]
        self.nCalls = data[9]

    def __str__(self):
        monitoring_data = {}
        callees = [{}]

        callees[0]["lineNumber"] = self.lineNumber
        callees[0]["nSamples"] = self.nSamples
        callees[0]["functionName"] = self.functionName
        callees[0]["nCalls"] = self.nCalls

        monitoring_data["commitHash"] = self.commitHash
        monitoring_data["id"] = self.id
        monitoring_data["publicIP"] = self.publicIP
        monitoring_data["timestamp"] = self.timestamp
        monitoring_data["application"] = self.application
        monitoring_data["macAddressHash"] = self.macAddressHash
        monitoring_data["callees"] = callees

        return str(monitoring_data)


class MonitoringDataFactory(factory.Factory):
    class Meta:
        model = MonitoringDataGenerator

    data = list()

    data.append("d0eb7082f4dd5dfce4c543e21299fb2e5774f70b")
    data.append("30d376d2-fc7e-10d5-d51fe33373fd")
    data.append("187.2.167.60")
    data.append(int(1531490785464))
    data.append("nugvjtNBxHbjBnqbcFZvjn")
    data.append("d1dd34825af8599b78bd5f4a1d7d186e")
    data.append(int(836))
    data.append(int(5745))
    data.append("root")
    data.append(0)
