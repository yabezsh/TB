/*
 * TbUTClusterCreator.h
 *
 *  Created on: Jan 5, 2015
 *      Author: ADendek
 */

#pragma once

#include "TbUTIClusterCreator.h"
#include "TbUTITresholdProvider.h"

namespace TbUT
{

class ClusterCreator: public IClusterCreator
{
public:
	ClusterCreator(const std::string&  p_sensorType, ITresholdProvider& p_thresholds);
	ClusterContainer::ClusterVector createClusters(RawData<double> *p_inputData);
	virtual ~ClusterCreator(){}

protected:
	 enum SensorType
	   {
	      P_TYPE,
	      N_TYPE,
	      CUSTOM
	   };

	typedef ClusterContainer::ClusterVector::iterator ClusterIterator;

	virtual void convertStringToSensorType(const std::string& p_sensorType);

	virtual void findCulsterSeeds(RawData<double> *p_inputData);
	virtual void removeDuplicatedSeeds(RawData<double> *p_inputData);
	virtual void extendClusterSeeds(RawData<double> *p_inputData);

	virtual bool isBiggerThanSeedThreshold(RawData<double>::DataType p_channelSignal, int p_channel) const;
	virtual Cluster createCluster(RawData<double> *p_inputData, int l_channelNumber) const;

	virtual bool arePartOfTheSameCluster(RawData<double>* p_inputData, ClusterIterator& p_firstIt, ClusterIterator& p_secondIt) const;
	virtual bool canBePartOfTheSameCluster(ClusterIterator& p_firstIt, ClusterIterator& p_secondIt) const;

	virtual void extendCluster(ClusterIterator& p_clusterIt, RawData<double>* p_inputData);
	virtual void removeClusterSeedWithSmallerCharge(ClusterIterator& p_firstIt, ClusterIterator& p_secondIt);
	virtual bool hasNotMaximumSize(ClusterIterator& p_clusterIt) const;
	virtual bool isStripNeedToBeAddedToCluster(ClusterIterator& p_clusterIt, RawData<double> *p_inputData,int p_stripShift, bool p_isCheckingLeft  ) const;
	virtual void updateCluster(ClusterIterator& p_clusterIt,RawData<double> *p_inputData ,int p_stripShift, bool p_isCheckingLeft);
	virtual bool isInvalidChannelNumber(int p_stripShift) const;
	virtual bool isBiggerThanLowThreshold(RawData<double>::DataType p_channelSignal, int p_chnnel) const;
	virtual void fillOuterStrips(RawData<double> *p_inputData);



	int m_clusterMaxSize;
	ITresholdProvider& m_thresholds;
	ClusterContainer::ClusterVector m_culsterVector;
	SensorType m_sensorType;

};


} /* namespace TbUT */

