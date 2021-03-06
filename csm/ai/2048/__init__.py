


import math

def evalscore(bd):
    
    info = bd.produceInfo()
    emptyCells = info[0]
    smoothWeight = 0.1

    mono2Weight  = 1.0
    emptyWeight  = 2.7
    maxWeight    = 1.0

    return bd.smoothness() * smoothWeight \
         + bd.monotonicity2() * mono2Weight \
         + math.log(emptyCells) * emptyWeight \
         + bd.grid.maxValue() * maxWeight
         #+ this.grid.monotonicity() * monoWeight
         #- this.grid.islands() * islandWeight


def search(bd, depth, alpha, beta, positions, cutoffs):
    bestScore = 0
    bestMove = -1
    result = 0
    
    # the maxing player
    if (bd.playerTurn): 
        bestScore = alpha
        for direction in [0, 1, 2, 3]:
            newGrid = bd.clone();
            if (newGrid.move(direction).moved):
                positions += 1
                if newGrid.isWin(): 
                    return { move: direction, score: 10000, positions: positions, cutoffs: cutoffs }
                
                var newAI = new AI(newGrid);
                
                if depth == 0:
                    result = { move: direction, score: newAI.eval() }
                else:
                    result = newAI.search(depth-1, bestScore, beta, positions, cutoffs)
                    if result.score > 9900 :# win
                        result.score -= 1# to slightly penalize higher depth from win
                    
                    positions = result.positions
                    cutoffs = result.cutoffs
                
                
                if result.score > bestScore:
                    bestScore = result.score
                    bestMove = direction
                
                if bestScore > beta: 
                    cutoffs += 1
                    return { move: bestMove, score: beta, positions: positions, cutoffs: cutoffs }

    else: # computer's turn, we'll do heavy pruning to keep the branching factor low
        bestScore = beta
        
        # try a 2 and 4 in each cell and measure how annoying it is
        # with metrics from eval
        candidates = []
        cells = this.grid.availableCells()
        scores = { 2: [], 4: [] }
        for value in scores:
            for var i in cells:
                scores[value].push(None)
                cell = cells[i]
                tile = new Tile(cell, parseInt(value, 10))
                this.grid.insertTile(tile)
                scores[value][i] = -this.grid.smoothness() + this.grid.islands()
                this.grid.removeTile(cell)
  
    
        # now just pick out the most annoying moves
        maxScore = Math.max(Math.max.apply(null, scores[2]), Math.max.apply(null, scores[4]));
        for value in scores: # 2 and 4
            for i=0; i<scores[value].length; i++:
                if (scores[value][i] == maxScore):
                    candidates.push( { position: cells[i], value: parseInt(value, 10) } )
       
    
        # search on each candidate
        for (var i=0; i<candidates.length; i++) {
            var position = candidates[i].position;
            var value = candidates[i].value;
            var newGrid = this.grid.clone();
            var tile = new Tile(position, value);
            newGrid.insertTile(tile);
            newGrid.playerTurn = true;
            positions++;
            newAI = new AI(newGrid);
            result = newAI.search(depth, alpha, bestScore, positions, cutoffs);
            positions = result.positions;
            cutoffs = result.cutoffs;
        
            if (result.score < bestScore) {
                bestScore = result.score;
            }
            if bestScore < alpha:
                cutoffs++;
                return { move: null, score: alpha, positions: positions, cutoffs: cutoffs };
        
     
    
    return { move: bestMove, score: bestScore, positions: positions, cutoffs: cutoffs };


// performs a search and returns the best move
AI.prototype.getBest = function() {
  return this.iterativeDeep();
}

// performs iterative deepening over the alpha-beta search
AI.prototype.iterativeDeep = function() {
  var start = (new Date()).getTime();
  var depth = 0;
  var best;
  do {
    var newBest = this.search(depth, -10000, 10000, 0 ,0);
    if (newBest.move == -1) {
      //console.log('BREAKING EARLY');
      break;
    } else {
      best = newBest;
    }
    depth++;
  } while ( (new Date()).getTime() - start < minSearchTime);
  //console.log('depth', --depth);
  //console.log(this.translate(best.move));
  //console.log(best);
  return best
}

AI.prototype.translate = function(move) {
 return {
    0: 'up',
    1: 'right',
    2: 'down',
    3: 'left'
  }[move];
}