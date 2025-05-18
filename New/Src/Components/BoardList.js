import React, { useEffect, useState } from 'react';
import api from '../api';

function BoardList() {
  const [boards, setBoards] = useState([]);

  useEffect(() => {
    api.get('/fetch-boards')
      .then(res => setBoards(res.data))
      .catch(err => console.error('Error fetching boards:', err));
  }, []);

  return (
    <div>
      <h2>Boards</h2>
      <ul>
        {boards.map(board => (
          <li key={board.id}>
            <strong>{board.name}</strong> (Owner: {board.owner_user_name})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BoardList;
