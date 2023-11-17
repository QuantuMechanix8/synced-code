using System;

public class pogram
{

	static void Main(string[] args)
	{
		uint size;
		bool turnX = true;
		Console.WriteLine("Welcome to the pogram");
		Console.Write("Please enter the desired size of the grid: ");
		while (!uint.TryParse(Console.ReadLine(), out size) || size<2)
		{
			Console.WriteLine("that was not a valid board size, please enter an integer above 1");
		}
		board gameBoard = new board(size,size);
		bool validMove;
		while (false==false)
		{
			char player = 'O';
			gameBoard.outputBoard();
			if(turnX)
			{
				player = 'X';
			}
			int x, y;
			do{
			Console.WriteLine($"\nIt's now {player}'s turn");
			Console.Write("Please enter your first co-ordinate: ");
			int.TryParse(Console.ReadLine(), out y);
			Console.Write("Please enter your second co-ordinate: ");
			int.TryParse(Console.ReadLine(), out x);
			Console.WriteLine($"{player} move ({x},{y})\n");
			validMove = gameBoard.addPiece(x,y,player);
			if (!validMove)
			{
				Console.Write($"Retry move\n\n");
			}} while (!validMove);
			// if(gameBoard.checkWin(player))
			// {
			// 	Console.WriteLine($"{player} wins the game!");
			// 	break;
			// }
			turnX = !turnX;
		}
			
	}
}

public class board
{
	private uint size;
	private char[,] grid;
	public board(uint Psize, uint numToWin)
	{
		size = Psize;
		grid = new char[size,size];
	}
	public void outputBoard()
	{
		for(int i=0; i<size; i++)
		{
			for(int j =0; j<size; j++)
			{
				if(grid[i,j]=='\0')
				{
				Console.Write($"|{grid[i,j]} ");
				}
				else
				{
					Console.Write($"|{grid[i,j]}");
				}
			}
			Console.Write("|\n");
		}
	}
	public bool addPiece(int x, int y, char player)
	{
		if((x>size-1 || x<0 ) || (y<0 || y>size-1))
		{
			Console.WriteLine($"{x}, {y} is not a valid space on the board! ");
			return false;
		}
		else if(grid[x,y]!= '\0')
		{
			if(player == grid[x,y])
			{
				Console.Write($"You've already moved to {x}, {y}!");
			}
			else
			{
				Console.Write($"Player {player} already has a peice at {x}, {y}!\n");
			}
			return false;
			
		}
		else
		{
			grid[x,y] = ' ';
			grid[x,y] = player;
			return true;
		}
	}
	public bool checkWin(char player)
	{
		for(uint i = 0; i<size; i++)
		{
			if((checkLine(i, 0, 0, 1)) == player)
			{
				return true;
			}
			if((checkLine(0, i, 1, 0)) == player)
			{
				return true;
			}
			if((checkLine(0, i, 1, 1)) == player)
			{
				return true;
			}
			if((checkLine(0, i, -1, 1)) == player)))
			{
				return true;
			}
		}
		return false;
	}
	public char checkLine(uint X, uint Y, int dY, int dX)
	{
		int numX = -dX;
		int numO =-dY;
		while(X<size && Y<size)
		{
			int nextX = (int)(X+dX);
			int nextY = (int)(Y+dY);
			if(grid[nextX, nextY]=='X')
			{
				numX++;
				numO = 0;
			}
			else if(grid[nextX, nextY]=='O')
			{
				numO++;
				numX = 0;
			}
		}
		if(numX==size)
		{
			return 'X';
		}
		else if(numO==size)
		{
			return 'O';
		}
		else
		{
			return ' ';
		}
	}
}
