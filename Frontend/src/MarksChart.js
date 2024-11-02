import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register the necessary components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const MarksChart = ({marksData}) => {
  // Dummy data
  const labels = marksData.map(item => item.StudentName);
  const data = marksData.map(item => item.Marks.reduce((acc, curr) => acc + curr, 0)); // Summing marks if there are multiple

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Marks",
        data: data,
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div>
      <h2>Student Marks</h2>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default MarksChart;
