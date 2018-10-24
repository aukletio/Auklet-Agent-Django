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
        return '{"commitHash": "%s", ' \
               '"id": "%s", ' \
               '"publicIP": "%s", ' \
               '"timestamp": %d, ' \
               '"application": "%s", ' \
               '"macAddressHash": "%s", ' \
               '"callees": ' \
               '[{"lineNumber": %d, ' \
               '"nSamples": %d, ' \
               '"functionName": "%s", ' \
               '"nCalls": %d}]}' \
               % (self.commitHash, self.id, self.publicIP,
                  self.timestamp, self.application, self.macAddressHash,
                  self.lineNumber, self.nSamples, self.functionName,
                  self.nCalls)


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


class ConfigGenerator(object):
    def __init__(self, data):
        self.brokers = data[0]
        self.prof_topic = data[1]
        self.event_topic = data[2]
        self.log_topic = data[3]
        self.user_metrics_topic = data[4]

    def __str__(self):
        return '{"brokers": ["%s"], "prof_topic": "%s", "event_topic": ' \
               '"%s", "log_topic": "%s", "user_metrics_topic": "%s"}' \
               % (self.brokers, self.prof_topic, self.event_topic,
                  self.log_topic, self.user_metrics_topic)


class ConfigFactory(factory.Factory):
    class Meta:
        model = ConfigGenerator

    data = list()

    data.append("http://api-staging.auklet.io:9093")
    data.append("profiling")
    data.append("events")
    data.append("logging")
    data.append("user_metrics")


class StackTraceGenerator(object):
    def __init__(self, data):
        self.functionName = data[0]
        self.lineNumber = data[1]
        self.nCalls = data[2]
        self.nSamples = data[3]

    def __str__(self):
        return '''{'callees': [],\n 'filePath': None,\n ''' \
               ''''functionName': '%s',\n 'lineNumber': %d,\n ''' \
               ''''nCalls': %d,\n 'nSamples': %d}''' \
               % (self.functionName, self.lineNumber,
                  self.nCalls, self.nSamples)


class StackTraceFactory(factory.Factory):
    class Meta:
        model = StackTraceGenerator

    data = list()

    data.append("root")
    data.append(1)
    data.append(1)
    data.append(1)


class SingleNestedStackGenerator(object):
    def __init__(self, data):
        self.callees_functionName = data[0]
        self.callees_lineNumber = data[1]
        self.callees_nCalls = data[2]
        self.callees_nSamples = data[3]
        self.functionName = data[4]
        self.lineNumber = data[5]
        self.nCalls = data[6]
        self.nSamples = data[7]

    def __str__(self):
        return '''{'callees': [{'callees': [],\n''' \
               '''              'filePath': None,\n''' \
               '''              'functionName': '%s',\n''' \
               '''              'lineNumber': %d,\n''' \
               '''              'nCalls': %d,\n''' \
               '''              'nSamples': %d}],\n 'filePath': None,\n''' \
               ''' 'functionName': '%s',\n 'lineNumber': %d,\n''' \
               ''' 'nCalls': %d,\n 'nSamples': %d}''' \
               % (self.callees_functionName, self.callees_lineNumber,
                  self.callees_nCalls, self.callees_nSamples,
                  self.functionName, self.lineNumber, self.nCalls,
                  self.nSamples)


class SingleNestedStackTraceFactory(factory.Factory):
    class Meta:
        model = SingleNestedStackGenerator

    data = list()

    data.append("")
    data.append(0)
    data.append(1)
    data.append(1)

    data.append("root")
    data.append(1)
    data.append(1)
    data.append(1)


class LimitsGenerator(object):
    def __init__(self, storage_limit="null", emission_period=60,
                 performance_metrics="true", user_metrics="false",
                 cellular_data_limit="null", normalized_cell_plan_date=1):
        self.storage_limit = str(storage_limit)
        self.emission_period = str(emission_period)
        self.performance_metrics = str(performance_metrics)
        self.user_metrics = str(user_metrics)
        self.cellular_data_limit = str(cellular_data_limit)
        self.normalized_cell_plan_data = str(normalized_cell_plan_date)

    def __str__(self):
        return """{"storage": {"storage_limit": """ + \
               self.storage_limit + \
               """}, "emission_period": """ + \
               self.emission_period + \
               """, "features": {"performance_metrics": """ + \
               self.performance_metrics + \
               """, "user_metrics": """ + \
               self.user_metrics + \
               """}, "data": {"cellular_data_limit": """ + \
               self.cellular_data_limit + \
               """, "normalized_cell_plan_date": """ + \
               self.normalized_cell_plan_data + \
               """}}"""
