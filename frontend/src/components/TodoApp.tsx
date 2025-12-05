import { useState, useEffect } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Trash2, CheckCircle2, Circle, CalendarIcon, Search, Tag, AlertCircle, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { format } from "date-fns";
import { api } from "@/api/client";
import { useAuth } from "@/context/AuthContext";
import { useToast } from "@/components/ui/use-toast";

type Priority = "low" | "medium" | "high";

type Todo = {
  id: string;
  text: string;
  completed: boolean;
  createdAt: number;
  dueDate: number | null;
  priority: Priority | null;
  category: string | null;
};

type Filter = "all" | "active" | "completed";

export const TodoApp = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [filter, setFilter] = useState<Filter>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedPriority, setSelectedPriority] = useState<Priority | null>(null);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [dueDate, setDueDate] = useState<Date | undefined>();
  const { logout, user } = useAuth();
  const { toast } = useToast();

  const fetchTodos = async () => {
    try {
      const data = await api.get('/todos');
      setTodos(data);
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to fetch todos",
      });
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const addTodo = async () => {
    if (inputValue.trim()) {
      try {
        const newTodo = await api.post('/todos', {
          text: inputValue.trim(),
          dueDate: dueDate ? dueDate.getTime() : null,
          priority: selectedPriority,
          category: selectedCategory.trim() || null,
        });
        setTodos([newTodo, ...todos]);
        setInputValue("");
        setSelectedPriority(null);
        setSelectedCategory("");
        setDueDate(undefined);
      } catch (error) {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to create todo",
        });
      }
    }
  };

  const toggleTodo = async (id: string) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    try {
      const updatedTodo = await api.patch(`/todos/${id}`, {
        completed: !todo.completed
      });
      setTodos(todos.map((t) => (t.id === id ? updatedTodo : t)));
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to update todo",
      });
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await api.delete(`/todos/${id}`);
      setTodos(todos.filter((todo) => todo.id !== id));
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to delete todo",
      });
    }
  };

  const clearCompleted = async () => {
    try {
      await api.delete('/todos/completed');
      setTodos(todos.filter((t) => !t.completed));
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to clear completed todos",
      });
    }
  };

  const filteredTodos = todos.filter((todo) => {
    // Filter by completion status
    if (filter === "active" && todo.completed) return false;
    if (filter === "completed" && !todo.completed) return false;

    // Filter by search query
    if (searchQuery && !todo.text.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false;
    }

    return true;
  });

  const getPriorityColor = (priority: Priority | null) => {
    switch (priority) {
      case "high": return "text-red-500 bg-red-500/10";
      case "medium": return "text-yellow-500 bg-yellow-500/10";
      case "low": return "text-green-500 bg-green-500/10";
      default: return "text-muted-foreground bg-secondary";
    }
  };

  const isOverdue = (dueDate: number | null) => {
    if (!dueDate) return false;
    return dueDate < Date.now();
  };

  const activeCount = todos.filter((t) => !t.completed).length;

  return (
    <div className="min-h-screen bg-gradient-app py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex justify-end mb-4">
          <Button variant="ghost" onClick={logout} className="text-muted-foreground hover:text-destructive">
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-2">
            My Tasks
          </h1>
          <p className="text-muted-foreground">
            Stay organized, one task at a time
          </p>
        </div>

        <div className="bg-card rounded-lg shadow-medium p-6 sm:p-8 animate-fade-in">
          {/* Search */}
          <div className="mb-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 transition-all duration-200 focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          {/* Add Todo Form */}
          <div className="space-y-4 mb-6 p-4 bg-secondary/30 rounded-lg">
            <Input
              type="text"
              placeholder="Add a new task..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addTodo()}
              className="transition-all duration-200 focus:ring-2 focus:ring-primary"
            />

            <div className="flex flex-wrap gap-2">
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="outline"
                    className={cn(
                      "justify-start text-left font-normal",
                      !dueDate && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {dueDate ? format(dueDate, "PPP") : "Due date"}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    selected={dueDate}
                    onSelect={setDueDate}
                    initialFocus
                    className={cn("p-3 pointer-events-auto")}
                  />
                </PopoverContent>
              </Popover>

              <Select value={selectedPriority || ""} onValueChange={(value) => setSelectedPriority(value as Priority)}>
                <SelectTrigger className="w-[140px]">
                  <SelectValue placeholder="Priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                </SelectContent>
              </Select>

              <Input
                type="text"
                placeholder="Category"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="flex-1 min-w-[120px]"
              />

              <Button
                onClick={addTodo}
                className="bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 hover:scale-105"
              >
                Add Task
              </Button>
            </div>
          </div>

          <div className="flex gap-2 mb-6 flex-wrap">
            {(["all", "active", "completed"] as Filter[]).map((f) => (
              <Button
                key={f}
                variant={filter === f ? "default" : "secondary"}
                size="sm"
                onClick={() => setFilter(f)}
                className={cn(
                  "capitalize transition-all duration-200",
                  filter === f
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary hover:bg-secondary/80"
                )}
              >
                {f}
              </Button>
            ))}
          </div>

          <div className="space-y-2">
            {filteredTodos.length === 0 ? (
              <div className="text-center py-12 text-muted-foreground animate-fade-in">
                <Circle className="w-16 h-16 mx-auto mb-4 opacity-30" />
                <p className="text-lg">
                  {filter === "completed"
                    ? "No completed tasks yet"
                    : filter === "active"
                      ? "No active tasks"
                      : "No tasks yet. Add one above!"}
                </p>
              </div>
            ) : (
              filteredTodos.map((todo, index) => (
                <div
                  key={todo.id}
                  className={cn(
                    "p-4 bg-secondary/50 rounded-lg hover:bg-secondary transition-all duration-200 group animate-slide-in",
                    isOverdue(todo.dueDate) && !todo.completed && "border-l-4 border-red-500"
                  )}
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <div className="flex items-start gap-3">
                    <Checkbox
                      id={todo.id}
                      checked={todo.completed}
                      onCheckedChange={() => toggleTodo(todo.id)}
                      className="mt-1 transition-all duration-200 data-[state=checked]:bg-primary data-[state=checked]:border-primary"
                    />
                    <div className="flex-1 space-y-2">
                      <label
                        htmlFor={todo.id}
                        className={cn(
                          "block cursor-pointer transition-all duration-200",
                          todo.completed
                            ? "line-through text-muted-foreground"
                            : "text-card-foreground"
                        )}
                      >
                        {todo.text}
                      </label>

                      <div className="flex flex-wrap gap-2 text-xs">
                        {todo.priority && (
                          <Badge variant="secondary" className={cn("capitalize", getPriorityColor(todo.priority))}>
                            <AlertCircle className="w-3 h-3 mr-1" />
                            {todo.priority}
                          </Badge>
                        )}
                        {todo.category && (
                          <Badge variant="secondary" className="bg-primary/10 text-primary">
                            <Tag className="w-3 h-3 mr-1" />
                            {todo.category}
                          </Badge>
                        )}
                        {todo.dueDate && (
                          <Badge
                            variant="secondary"
                            className={cn(
                              isOverdue(todo.dueDate) && !todo.completed
                                ? "bg-red-500/10 text-red-500"
                                : "bg-secondary text-muted-foreground"
                            )}
                          >
                            <CalendarIcon className="w-3 h-3 mr-1" />
                            {format(new Date(todo.dueDate), "MMM d, yyyy")}
                          </Badge>
                        )}
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => deleteTodo(todo.id)}
                      className="opacity-0 group-hover:opacity-100 transition-all duration-200 hover:bg-destructive/10 hover:text-destructive"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>

          {todos.length > 0 && (
            <div className="mt-6 pt-6 border-t border-border flex justify-between items-center text-sm text-muted-foreground animate-fade-in">
              <span>
                {activeCount} {activeCount === 1 ? "task" : "tasks"} remaining
              </span>
              <Button
                variant="ghost"
                size="sm"
                onClick={clearCompleted}
                className="hover:text-destructive transition-colors duration-200"
              >
                Clear completed
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
