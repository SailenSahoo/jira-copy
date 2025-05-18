import React, { useState } from 'react';
import IssueList from './components/IssueList';
import ProjectList from './components/ProjectList';
import BoardList from './components/BoardList';

function App() {
  const [searchKey, setSearchKey] = useState('');

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Jira Clone Dashboard</h1>

      <input
        type="text"
        placeholder="Search by Issue Key"
        value={searchKey}
        onChange={(e) => setSearchKey(e.target.value)}
        style={{ padding: '8px', width: '300px', marginBottom: '20px' }}
      />

      <IssueList searchKey={searchKey} />
      <hr />
      <ProjectList />
      <hr />
      <BoardList />
    </div>
  );
}

export default App;
