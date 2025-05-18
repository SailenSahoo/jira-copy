import React from 'react';

const SearchBar = ({ value, onChange }) => {
  return (
    <input
      type="text"
      placeholder="Search by Issue Key"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      style={{ width: '300px', padding: '8px', marginBottom: '20px' }}
    />
  );
};

export default SearchBar;
