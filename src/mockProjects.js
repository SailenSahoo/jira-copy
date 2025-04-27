const mockProjects = [
    {
      name: 'Migration Project',
      issues: [
        { key: 'MP-1', summary: 'Migrate to new system', customFields: { status: 'Done', priority: 'High' } },
        { key: 'MP-2', summary: 'Data cleanup', customFields: { status: 'In Progress', priority: 'Medium' } }
      ]
    },
    {
      name: 'Bug Fixes Q2',
      issues: [
        { key: 'BFQ2-1', summary: 'Fix login bug', customFields: { status: 'To Do', priority: 'High' } },
        { key: 'BFQ2-2', summary: 'Resolve UI glitch', customFields: { status: 'Done', priority: 'Low' } }
      ]
    }
  ];
  
  export default mockProjects;
  