#ifndef TBKALMANTRACK_H
#define TBKALMANTRACK_H

#include "Event/TbTrack.h"

namespace LHCb {
class TbKalmanNode;

class TbKalmanTrack : public TbTrack {
 public:
  /// Constructor
  TbKalmanTrack(const LHCb::TbTrack& track, const double hiterror2, 
                const double noise2);
  // Destructor
  ~TbKalmanTrack();

  // get the nodes
  const std::vector<TbKalmanNode*>& nodes() const { return m_nodes; }

  // called by daughter node if something changes
  void resetCache() {}

  // fit
  void fit();

  // dump some debug info
  void print() const;

  // add a node
  void addNode(TbKalmanNode*);

  // add a 'reference' node (without a measurement, just to have the state)
  void addReferenceNode(double z);

  // deactivate a measurement on the track
  void deactivateCluster(const TbCluster& clus);

 private:
  std::vector<TbKalmanNode*> m_nodes;
};
}

#endif
