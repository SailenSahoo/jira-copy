import React, { useEffect, useState } from 'react';
import { fetchIssues } from './services/api';
import SearchBar from './components/SearchBar';
import IssueList from './components/IssueList';

function App() {
  const [issues, setIssues] = useState([]);
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    fetchIssues().then(setIssues);
  }, []);

  const filteredIssues = issues.filter((issue) =>
    `${issue.pkey}-${issue.issuenum}`.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <div style={{ padding: '20px' }}>
      <h2>Jira Issues</h2>
      <SearchBar value={searchText} onChange={setSearchText} />
      <IssueList issues={filteredIssues} />
    </div>
  );
}

export default App;
