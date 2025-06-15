import { useState } from 'react';
import './index.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold bg-gradient-to-r from-sky-500 to-fuchsia-600 text-transparent bg-clip-text">Starkverse Dashboard</h1>
      <button className="mt-4 p-2 bg-blue-600 rounded" onClick={() => setCount((c) => c + 1)}>Count {count}</button>
    </div>
  );
}

export default App;
