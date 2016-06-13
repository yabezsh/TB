/*
 * TbUTClusterCreatorFiveStrips.h
 *
 *  Created on: Jun 6, 2016
 *      Author: adendek
 */
#pragma once

#include "TbUTClusterCreator.h"

namespace TbUT {

class ClusterCreatorFiveStrips: public ClusterCreator {
public:
	ClusterCreatorFiveStrips(const std::string&  p_sensorType, ITresholdProvider& p_thresholds):
		ClusterCreator(p_sensorType, p_thresholds)
	{}

	virtual ~ClusterCreatorFiveStrips(){};

private:
	void extendClusterSeeds(RawData<double> *p_inputData);
};

}
