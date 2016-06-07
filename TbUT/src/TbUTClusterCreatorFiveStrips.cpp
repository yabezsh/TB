#include "TbUTClusterCreatorFiveStrips.h"



using namespace TbUT;

void ClusterCreatorFiveStrips::extendClusterSeeds(RawData<double> *p_inputData)
{
	std::vector<int> relativePostitions={-2,-1,1,2};
	for(auto& cluster :  ClusterCreator::m_culsterVector){
		int seedPosition = cluster.m_seedPosition;
		cluster.m_position = cluster.m_seedPosition;
		for(auto relativePosition : relativePostitions){
			int stripPostion = seedPosition+relativePosition;
			if(!ClusterCreator::isInvalidChannelNumber(stripPostion)){
				auto charge = p_inputData->getSignal(stripPostion);
				cluster.m_size+=1;
				cluster.m_charge+=charge;

			}
		}
	}
}
