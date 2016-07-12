/*
 * TbUTICommonModeSubtractor.h
 *
 *  Created on: Nov 23, 2014
 *      Author: ADendek
 */
#pragma once

#include "TbUTIProcessingEngine.h"
#include <map>

namespace TbUT
{

class ICommonModeSubtractor : public IProcessingEngine<int, double>
{
public:
	virtual ~ICommonModeSubtractor(){};
	virtual std::map<int, double> getCorrectionMap() = 0;
	virtual std::map<int, int> getUsedChannelMap() = 0;

};

}


