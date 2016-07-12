/*
 * TbUTCMSCorrections.h
 *
 *  Created on: Jul 12, 2016
 *      Author: adendek
 */

#pragma once

#include "GaudiKernel/DataObject.h"
#include <map>



namespace TbUT {

struct CMSCorrections
{
	CMSCorrections(){};
	std::map<int, double> getCorrectionMap(){return m_correctionPerBeetle;}
	std::map<int, int> getUsedChannelMap(){return m_usedChannelPerBeetle;}

	void setCorrectionMap(std::map<int, double> p_map){m_correctionPerBeetle= p_map;}
	void setUsedMap(std::map<int, int> p_map){m_usedChannelPerBeetle= p_map;}

private:
	std::map<int, double> m_correctionPerBeetle;
	std::map<int, int> m_usedChannelPerBeetle;
};




class CMSCorrectionsContainer : public DataObject
{
public:
	typedef std::vector<CMSCorrections>  CMSCorrenctionVec;


	CMSCorrectionsContainer():
		empty(true),
		m_dataVector()
	{};

	void addData(CMSCorrections cmsCorrection)
	{
		m_dataVector.push_back(cmsCorrection);
		empty=false;
	}
	bool isEmpty(){return empty;}
	CMSCorrenctionVec getData(){return m_dataVector;}

private:
	bool empty;
	CMSCorrenctionVec m_dataVector;

};

} /* namespace TbUT */

