import re

test = '''
ValidSearchAttributes:                    dc.GetMapProperty(dynamicconfig.ValidSearchAttributes),
		SearchAttributesNumberOfKeysLimit:        dc.GetIntPropertyFilteredByDomain(dynamicconfig.SearchAttributesNumberOfKeysLimit),
		SearchAttributesSizeOfValueLimit:         dc.GetIntPropertyFilteredByDomain(dynamicconfig.SearchAttributesSizeOfValueLimit),
		SearchAttributesTotalSizeLimit:           dc.GetIntPropertyFilteredByDomain(dynamicconfig.SearchAttributesTotalSizeLimit),
		StickyTTL:                                dc.GetDurationPropertyFilteredByDomain(dynamicconfig.StickyTTL),
		DecisionHeartbeatTimeout:                 dc.GetDurationPropertyFilteredByDomain(dynamicconfig.DecisionHeartbeatTimeout),
		DecisionRetryCriticalAttempts:            dc.GetIntProperty(dynamicconfig.DecisionRetryCriticalAttempts),
		DecisionRetryMaxAttempts:                 dc.GetIntPropertyFilteredByDomain(dynamicconfig.DecisionRetryMaxAttempts),
		NormalDecisionScheduleToStartMaxAttempts: dc.GetIntPropertyFilteredByDomain(dynamicconfig.NormalDecisionScheduleToStartMaxAttempts),
		NormalDecisionScheduleToStartTimeout:     dc.GetDurationPropertyFilteredByDomain(dynamicconfig.NormalDecisionScheduleToStartTimeout),

		ReplicationTaskFetcherParallelism:                  dc.GetIntProperty(dynamicconfig.ReplicationTaskFetcherParallelism),
		ReplicationTaskFetcherAggregationInterval:          dc.GetDurationProperty(dynamicconfig.ReplicationTaskFetcherAggregationInterval),
		ReplicationTaskFetcherTimerJitterCoefficient:       dc.GetFloat64Property(dynamicconfig.ReplicationTaskFetcherTimerJitterCoefficient),
		ReplicationTaskFetcherErrorRetryWait:               dc.GetDurationProperty(dynamicconfig.ReplicationTaskFetcherErrorRetryWait),
		ReplicationTaskFetcherServiceBusyWait:              dc.GetDurationProperty(dynamicconfig.ReplicationTaskFetcherServiceBusyWait),
		ReplicationTaskFetcherEnableGracefulSyncShutdown:   dc.GetBoolProperty(dynamicconfig.ReplicationTaskFetcherEnableGracefulSyncShutdown),
		ReplicationTaskProcessorErrorRetryWait:             dc.GetDurationPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorErrorRetryWait),
		ReplicationTaskProcessorErrorRetryMaxAttempts:      dc.GetIntPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorErrorRetryMaxAttempts),
		ReplicationTaskProcessorErrorSecondRetryWait:       dc.GetDurationPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorErrorSecondRetryWait),
		ReplicationTaskProcessorErrorSecondRetryMaxWait:    dc.GetDurationPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorErrorSecondRetryMaxWait),
		ReplicationTaskProcessorErrorSecondRetryExpiration: dc.GetDurationPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorErrorSecondRetryExpiration),
		ReplicationTaskProcessorNoTaskRetryWait:            dc.GetDurationPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorNoTaskInitialWait),
		ReplicationTaskProcessorCleanupInterval:            dc.GetDurationPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorCleanupInterval),
		ReplicationTaskProcessorCleanupJitterCoefficient:   dc.GetFloat64PropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorCleanupJitterCoefficient),
		ReplicationTaskProcessorStartWait:                  dc.GetDurationPropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorStartWait),
		ReplicationTaskProcessorStartWaitJitterCoefficient: dc.GetFloat64PropertyFilteredByShardID(dynamicconfig.ReplicationTaskProcessorStartWaitJitterCoefficient),
		ReplicationTaskProcessorHostQPS:                    dc.GetFloat64Property(dynamicconfig.ReplicationTaskProcessorHostQPS),
		ReplicationTaskProcessorShardQPS:                   dc.GetFloat64Property(dynamicconfig.ReplicationTaskProcessorShardQPS),
		ReplicationTaskGenerationQPS:                       dc.GetFloat64Property(dynamicconfig.ReplicationTaskGenerationQPS),
		EnableReplicationTaskGeneration:                    dc.GetBoolPropertyFilteredByDomainIDAndWorkflowID(dynamicconfig.EnableReplicationTaskGeneration),
		EnableRecordWorkflowExecutionUninitialized:         dc.GetBoolPropertyFilteredByDomain(dynamicconfig.EnableRecordWorkflowExecutionUninitialized),
'''

rx = r'GetBoolProperty.*EnableRecordWorkflowExecutionUninitialized'

matches = re.findall(rx, test)
print(matches)