// src/pages/Issues.jsx
import React from "react";
import { useParams } from "react-router-dom";
import IssueCard from "../components/IssueCard";

const Issues = () => {
  const { projectKey } = useParams();

  // Temporary mocked issues (will be fetched from backend later)
  const issues = [
    {
      key: `${projectKey}-1`,
      summary: "Set up cloud project",
      type: "Task",
      status: "Done",
      assignee: "Alice",
      reporter: "Bob",
      priority: "High",
      created: "2023-01-10",
      description: "Initial setup for the new cloud Jira project.",
      customFields: [
        { name: "Business Unit", value: "Cloud Ops" },
        { name: "Impact", value: "High" }
      ],
      comments: [
        {
          author: "Carol",
          date: "2023-01-12",
          text: "This is almost done."
        },
        {
          author: "David",
          date: "2023-01-13",
          text: "Please update the assignee."
        }
      ]
    },
    {
      key: `${projectKey}-2`,
      summary: "Migrate user data",
      type: "Story",
      status: "In Progress",
      assignee: "Eve",
      reporter: "Frank",
      priority: "Medium",
      created: "2023-01-15",
      description: "Migration of all user-related data to the cloud.",
      customFields: [
        { name: "Team", value: "Data Migration" },
        { name: "Sprint", value: "Sprint 5" }
      ],
      comments: []
    }
  ];

  return (
    <div style={{ padding: "20px" }}>
      <h2>Issues for Project: {projectKey}</h2>
      {issues.map((issue, idx) => (
        <IssueCard key={idx} issue={issue} />
      ))}
    </div>
  );
};

export default Issues;
