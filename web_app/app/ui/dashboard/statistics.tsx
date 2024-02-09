"use client";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

export function ServicesStatistic({
  labels,
  data,
}: {
  labels: string[];
  data: number[];
}) {
  const options = {
    indexAxis: "y" as const,
    elements: {
      bar: {
        borderWidth: 2,
      },
    },
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "服務總預約人次",
      },
    },
  };

  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );

  return (
    <div className="w-1/2">
      <Bar
        data={{
          labels: labels,
          datasets: [
            {
              label: "預約數",
              data: data,
              backgroundColor: ["rgba(99, 99, 132, 0.2)"],
              borderColor: ["rgba(99, 99, 132, 1)"],
              borderWidth: 1,
            },
          ],
        }}
        options={options}
      />
    </div>
  );
}

export function GroupsStatistic({
  labels,
  data,
}: {
  labels: string[];
  data: number[];
}) {
  const options = {
    indexAxis: "x" as const,
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: "各群組成員數",
      },
    },
    scales: {
      y: {
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
  );

  return (
    <div className="w-1/2">
      <Bar
        data={{
          labels: labels,
          datasets: [
            {
              label: "成員數",
              data: data,
              backgroundColor: ["rgba(99, 255, 132, 0.2)"],
              borderColor: ["rgba(99, 255, 132, 1)"],
              borderWidth: 1,
            },
          ],
        }}
        options={options}
      />
    </div>
  );
}
