package student_player;

import java.util.List;

import boardgame.Board;
import boardgame.Move;
import coordinates.Coord;
import coordinates.Coordinates;
import tablut.TablutBoardState;
import tablut.TablutMove;
import tablut.TablutPlayer;

/** A player file submitted by a student. */
public class StudentPlayer extends TablutPlayer {

    /**
     * You must modify this constructor to return your student number. This is
     * important, because this is what the code that runs the competition uses to
     * associate you with your agent. The constructor should do nothing else.
     */
	private static int maxlevel=4;
	private static final int BLACK=TablutBoardState.MUSCOVITE;
	private static final int WHITE=TablutBoardState.SWEDE;
	private static final int B_LOOSE=-100;
	private static final int B_WIN=+100;
	private static final int MIN_INF=-10000;
	private static final int PLUS_INF=+10000;
	private static final int TIMEOUT=1850000000;
	private int me;
	private boolean slow=false;
	private double bestValue=MIN_INF;
    public StudentPlayer() {
        super("260809135");
    }
    

    /**
     * This is the primary method that you need to implement. The ``boardState``
     * object contains the current state of the game, which your agent must use to
     * make decisions.
     */
    public Move chooseMove(TablutBoardState boardState) {
        // You probably will make separate functions in MyTools.
        // For example, maybe you'll need to load some pre-processed best opening
        // strategies...
    	TablutMove bestMove;
    	List<TablutMove> options = boardState.getAllLegalMoves();
    	if(options.size()<30 && !slow ) {
    		maxlevel=5;
    		System.out.print("maxlevel=5\n");
    	}
    	else {
    		maxlevel=4;
    	}
    	
    	
    	me=player_id;
    	if(me==WHITE) {
    		bestValue=PLUS_INF;
    		bestMove= getBestWhiteMove(boardState,0);
    	}
    	else {
    		bestValue=MIN_INF;
    		bestMove= getBestBlackMove(boardState,0);
    	}
    	return bestMove;
    }
    
    private TablutMove getBestWhiteMove(TablutBoardState boardState, int level) {
    	double value=0;
    	long startTime = System.nanoTime();
    	
    	TablutMove bestMove=null;
    	List<TablutMove> options = boardState.getAllLegalMoves();

    	for (TablutMove move : options) {
    		TablutBoardState bsClone= (TablutBoardState) boardState.clone();
    		bsClone.processMove(move);
	    	if(bsClone.getWinner() ==WHITE) {
	    		return move;
	    	}
			value=maxValue(bsClone,MIN_INF,PLUS_INF,level+1);
    		if (value<bestValue) {
    			bestValue=value;
    			bestMove=move;
    		}
    		else if (value==bestValue) {
    			double r= Math.random();
    			if(r>0.5) {
    				bestValue=value;
	    			bestMove=move;
    			}
    		}
    		if( System.nanoTime()-startTime>TIMEOUT) {
    			System.out.print("not enough time\n");
    			System.out.print("BF was "+options.size()+"\n");
    			slow=true;
    			return bestMove;
    		}
    		//System.out.print("current value= "+ value+"\n");
    	}  	
    	
    	if(bestValue==B_WIN && level<=maxlevel) {
    		level++;
    		bestMove=getBestWhiteMove(boardState,level);
    	}
        return bestMove;
    }
    
    private TablutMove getBestBlackMove(TablutBoardState boardState, int level) {
    	double value=0;
    	long startTime = System.nanoTime();

    	TablutMove bestMove=null;
    	List<TablutMove> options = boardState.getAllLegalMoves();

    	for (TablutMove move : options) {
    		TablutBoardState bsClone= (TablutBoardState) boardState.clone();
    		bsClone.processMove(move);

	    	if (bsClone.getWinner() == BLACK) {
	    		return move;
	    	}
			value=minValue(bsClone,MIN_INF,PLUS_INF,level+1);
    		if (value>bestValue) {
    			bestValue=value;
    			bestMove=move;
    		}
    		else if (value==bestValue) {
    			double r= Math.random();
    			if(r>0.5) {
    				bestValue=value;
	    			bestMove=move;
    			}
    		}
    		if( System.nanoTime()-startTime>TIMEOUT) {
    			System.out.print("not enough time\n");
    			System.out.print("BF was "+options.size()+"\n");
    			return bestMove;
    		}
    		//System.out.print("current value= "+ value+"\n");
    	}
    	
            // Return your move to be processed by the server.
    	if(bestValue==B_LOOSE && level<=maxlevel) {
    		level++;
    		bestMove=getBestBlackMove(boardState,level);
    		System.out.print("keep trying level = " + level+" bestValue= "+bestValue+"\n");
    	}
        return bestMove;
    }
    private double maxValue(TablutBoardState bs, double alpha,double beta,int level) {
    	level++;
    	//System.out.print("level = "+level+"\n");
    	if (level>=maxlevel || bs.getWinner()!=Board.NOBODY) {
    		return evaluation(bs);
    	}
    	List<TablutMove> options = bs.getAllLegalMoves();
    	for (TablutMove move : options) {
    		TablutBoardState bsClone= (TablutBoardState) bs.clone();
    		bsClone.processMove(move);

    		alpha= Math.max(alpha,minValue(bsClone,alpha,beta,level));
    		if (alpha>=beta) {
    			return beta;
    		}
    	}

    	//System.out.print("max-alpha = "+alpha+"\n");
    	//System.out.print("max-beta = "+beta+"\n");
    	return alpha;
    }
    
    private double minValue(TablutBoardState bs, double alpha,double beta,int level) {
    	level++;
    	if (level>=maxlevel || bs.getWinner()!=Board.NOBODY) {
    		return evaluation(bs);
    	}
    	
    	List<TablutMove> options = bs.getAllLegalMoves();
    	for (TablutMove move : options) {
    		TablutBoardState bsClone= (TablutBoardState) bs.clone();
    		bsClone.processMove(move);

    		beta= Math.min(beta,maxValue(bsClone,alpha,beta,level));
    		if (alpha>=beta) {
    			return alpha;
    		}
    	}
    	return beta;
    }

    private double evaluation(TablutBoardState bs) {
    	double score = 0;
    	int blackPieces=0;
    	int whitePieces=0;
    	if(bs.getTurnNumber()>TablutBoardState.MAX_TURNS) {
    		score=0;
    	}
    	else if (bs.getWinner() == BLACK) {
    		score=B_WIN;
    	}
    	else if(bs.getWinner() == WHITE) {
    		score=B_LOOSE;
    	}
    	else if(bs.gameOver()) {
    		score=0;    		
    	}
    	else{
    		blackPieces=bs.getNumberPlayerPieces(BLACK);
    		whitePieces=bs.getNumberPlayerPieces(WHITE);
    		score=0.5*blackPieces-whitePieces;
    	
	    	score+=kingBlockScore(bs)*0.8;
    	}
    	return score;
    }
    private int kingBlockScore(TablutBoardState bs) {
    	int score=0;
    	int score1=-1;
    	int score2=-1;
    	int score3=-1;
    	int score4=-1;
    	int SurScore=0;
    	Coord king = bs.getKingPosition();
    	for(int i=0;i<king.x;i++) {
    		score1=-1;
    		if(bs.getPieceAt(i, king.y)==TablutBoardState.Piece.BLACK) {
    			score1=1;
    			break;
    		}
    	}
    	for(int i=king.x+1;i<9;i++) {
    		score2=-1;
    		if(bs.getPieceAt(i, king.y)==TablutBoardState.Piece.BLACK) {
    			score2=1;
    			break;
    		}
    	}
    	for(int j=0;j<king.y;j++) {
    		score3=-1;
    		if(bs.getPieceAt(king.x, j)==TablutBoardState.Piece.BLACK) {
    			score3=1;
    			break;
    		}
    	}
    	for(int j=king.y+1;j<9;j++) {
    		score4=-1;
    		if(bs.getPieceAt(king.x, j)==TablutBoardState.Piece.BLACK) {
    			score4=1;
    			break;
    		}
    	}
    	List<Coord> arroundKing= Coordinates.getNeighbors(king);
    	for( Coord c:arroundKing) {
    		SurScore=0;
    		if(bs.getPieceAt(c)==TablutBoardState.Piece.BLACK) {
    			SurScore++;
    			break;
    		}
    	}
    	score=score1+score2+score3+score4+SurScore/10;
    	return score;
    }
}
	
