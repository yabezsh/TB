#pragma once

#include "TbUTICommonModeSubtractor.h"
#include "TbUTIChannelMaskProvider.h"
#include "TbUTCMSCorrections.h"

#include <map>

namespace TbUT
{
    class CMSIterativelyPerBeetle : public  ICommonModeSubtractor
    {
    public:
        CMSIterativelyPerBeetle(IChannelMaskProvider& p_masksProvider );
        void processEvent(RawData<>* p_data, RawData<double> **p_output);

    	std::map<int, double> getCorrectionMap(){
    		return m_cumulcatedCorrectionPerBeetle;
    	}
    	std::map<int, int> getUsedChannelMap(){
    		return m_usedChannelPerBeetle;
    	}

    private:
	template<typename DATA_TYPE>
        void calculateCorrection(RawData<DATA_TYPE>* p_inputData);
	template<typename INPUT_DATA_TYPE, typename OUTPUT_TYPE_NAME>
        void removeCM(RawData<INPUT_DATA_TYPE>* p_data, RawData<OUTPUT_TYPE_NAME> **p_output);
        void resetMaps();
        void resetCMSCorrection();

        void initializeCorrectionAndHitMaps();

        IChannelMaskProvider& m_masksProvider;
        const int m_channelNumber;
        const int m_channelPerBeetle;
    	std::map<int, double> m_correctionPerBeetle;
    	std::map<int, double> m_cumulcatedCorrectionPerBeetle;
    	std::map<int, int> m_usedChannelPerBeetle;
    	std::map<int, double> m_hitThresholdPerBeetle;
    };
}



