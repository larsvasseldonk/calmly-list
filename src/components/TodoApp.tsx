import { useState, useEffect } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Trash2, CheckCircle2, Circle } from "lucide-react";
import { cn } from "@/lib/utils";

type Todo = {
  id: string;
  text: string;
  completed: boolean;
  createdAt: number;
};

type Filter = "all" | "active" | "completed";

export const TodoApp = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [filter, setFilter] = useState<Filter>("all");

  useEffect(() => {
    const stored = localStorage.getItem("todos");
    if (stored) {
      setTodos(JSON.parse(stored));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem("todos", JSON.stringify(todos));
  }, [todos]);

  const addTodo = () => {
    if (inputValue.trim()) {
      const newTodo: Todo = {
        id: Date.now().toString(),
        text: inputValue.trim(),
        completed: false,
        createdAt: Date.now(),
      };
      setTodos([newTodo, ...todos]);
      setInputValue("");
    }
  };

  const toggleTodo = (id: string) => {
    setTodos(
      todos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const deleteTodo = (id: string) => {
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  const filteredTodos = todos.filter((todo) => {
    if (filter === "active") return !todo.completed;
    if (filter === "completed") return todo.completed;
    return true;
  });

  const activeCount = todos.filter((t) => !t.completed).length;

  return (
    <div className="min-h-screen bg-gradient-app py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-4xl sm:text-5xl font-bold text-foreground mb-2">
            My Tasks
          </h1>
          <p className="text-muted-foreground">
            Stay organized, one task at a time
          </p>
        </div>

        <div className="bg-card rounded-lg shadow-medium p-6 sm:p-8 animate-fade-in">
          <div className="flex gap-2 mb-6">
            <Input
              type="text"
              placeholder="Add a new task..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addTodo()}
              className="flex-1 transition-all duration-200 focus:ring-2 focus:ring-primary"
            />
            <Button
              onClick={addTodo}
              className="bg-primary hover:bg-primary/90 text-primary-foreground transition-all duration-200 hover:scale-105"
            >
              Add
            </Button>
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
                  className="flex items-center gap-3 p-4 bg-secondary/50 rounded-lg hover:bg-secondary transition-all duration-200 group animate-slide-in"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <Checkbox
                    id={todo.id}
                    checked={todo.completed}
                    onCheckedChange={() => toggleTodo(todo.id)}
                    className="transition-all duration-200 data-[state=checked]:bg-primary data-[state=checked]:border-primary"
                  />
                  <label
                    htmlFor={todo.id}
                    className={cn(
                      "flex-1 cursor-pointer transition-all duration-200",
                      todo.completed
                        ? "line-through text-muted-foreground"
                        : "text-card-foreground"
                    )}
                  >
                    {todo.text}
                  </label>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => deleteTodo(todo.id)}
                    className="opacity-0 group-hover:opacity-100 transition-all duration-200 hover:bg-destructive/10 hover:text-destructive"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
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
                onClick={() => setTodos(todos.filter((t) => !t.completed))}
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
