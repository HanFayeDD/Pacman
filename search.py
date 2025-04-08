# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from queue import Queue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # 开始就是终点
    if problem.isGoalState(problem.getStartState()):
        return []

    # 开始不是终点
    stack = [(problem.getStartState(), [])]
    visited_set = set()
    while stack:
        now_state, now_route = stack.pop()
        if problem.isGoalState(now_state):
            print("到达终点")
            break
        if now_state in visited_set:
            continue
        visited_set.add(now_state)
        ls_successors = problem.getSuccessors(now_state)
        # 所有的节点都访问过，那就直接pop，不压入栈，也相当于搜索路线回退
        for next_state, action, _ in ls_successors:
            if next_state not in visited_set:
                next_route = []
                next_route.extend(now_route.copy())
                next_route.append(action)
                stack.append((next_state, next_route))
    return now_route


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    q = Queue()
    if problem.isGoalState(problem.getStartState()):
        return []

    q.put((problem.getStartState(), []))
    visited_set = set()
    while not q.empty():
        now_state, now_route = q.get()
        visited_set.add(now_state)
        if problem.isGoalState(now_state):
            print("到达终点")
            break
        ls_successors = problem.getSuccessors(now_state)
        for next_state, action, _ in ls_successors:
            if next_state not in visited_set:
                visited_set.add(next_state)  # 避免一个8字型的交叉节点被重复添加进队列中
                next_route = []
                next_route.extend(now_route.copy())
                next_route.append(action)
                q.put((next_state, next_route))
    return now_route


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # 初始化优先队列，存储(状态, 路径, 总代价)元组
    pq = PriorityQueue()
    start_state = problem.getStartState()
    pq.push((start_state, [], 0), 0)  # (state, actions, total_cost), priority

    visited = set()  # 记录已访问的状态

    while not pq.isEmpty():
        current_state, actions, current_cost = pq.pop()

        # 检查是否到达目标状态
        if problem.isGoalState(current_state):
            return actions

        if current_state not in visited:
            visited.add(current_state)

            # 获取所有后继状态
            for next_state, action, step_cost in problem.getSuccessors(current_state):
                if next_state not in visited:
                    # 计算新的总代价
                    new_cost = current_cost + step_cost
                    # 创建新的动作序列
                    new_actions = actions + [action]
                    # 按总代价作为优先级加入队列
                    pq.push((next_state, new_actions, new_cost), new_cost)

    return []  # 如果没有找到路径，返回空列表


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue
    
    # 初始化优先队列
    frontier = PriorityQueue()
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), 0)  # (state, actions, cost), priority
    
    # 使用字典记录到达每个状态的最小代价
    visited = {}
    visited[start_state] = 0
    
    while not frontier.isEmpty():
        current_state, actions, current_cost = frontier.pop()
        
        # 如果当前节点的代价大于已记录的最小代价，跳过
        if current_cost > visited.get(current_state, float('inf')):
            continue
            
        if problem.isGoalState(current_state):
            return actions
            
        for next_state, action, step_cost in problem.getSuccessors(current_state):
            new_cost = current_cost + step_cost
            # 如果新状态未被访问过
            # 或者新代价更小, 即新找到的路径更优
            if next_state not in visited or new_cost < visited[next_state]:
                new_actions = actions + [action]
                priority = new_cost + heuristic(next_state, problem)
                frontier.push((next_state, new_actions, new_cost), priority)
                visited[next_state] = new_cost
    return []



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
