/*
 * TbUTClusterCreatorSingleStrip.h
 *
 *  Created on: Jun 6, 2016
 *      Author: adendek
 */

#pragma once

#include "TbUTClusterCreator.h"

namespace TbUT
{
class ClusterCreatorSingleStrip: public ClusterCreator
{
public:
	ClusterCreatorSingleStrip(const std::string&  p_sensorType, ITresholdProvider& p_thresholds):
		ClusterCreator(p_sensorType, p_thresholds)
		{}

private :
	void extendClusterSeeds(RawData<double> *p_inputData){};
};
}

