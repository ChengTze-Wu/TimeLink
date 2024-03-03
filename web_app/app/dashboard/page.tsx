import { Metadata } from "next";
// import {
//   ServicesStatistic,
//   GroupsStatistic,
// } from "@/app/ui/dashboard/statistics";
// import { BillboardCard } from "@/app/ui/dashboard/billboard";
// import { getJson } from "@/app/lib/fetch-api-data";
// import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Dashboard",
};

// type ServiceResp = {
//   data: {
//     id: number;
//     name: string;
//     appointments: {}[];
//   }[];
// };

// type GroupResp = {
//   data: {
//     id: number;
//     name: string;
//     users: {}[];
//   }[];
// };

export default async function Page() {
  // const userInfo = cookies().get("user_info")?.value;
  // const user = JSON.parse(userInfo || "{}");
  // if (user?.role == "group_member") {
  //   redirect("/dashboard/bookings");
  // }
  // return (
  //   <main>
  //     <div className="flex flex-col h-full gap-10">
  //       <div className="flex h-1/4 gap-12">
  //         <BillboardCard title="總預約數" value={5} />
  //         <BillboardCard title="總成員數" value={5} />
  //       </div>
  //       {/* <div className="flex h-3/4">
  //         <ServicesStatistic
  //           labels={servicesStatlabels}
  //           data={servicesStatdata}
  //         />
  //         <GroupsStatistic labels={groupsStatlabels} data={groupsStatdata} />
  //       </div> */}
  //     </div>
  //   </main>
  // );
  redirect("/dashboard/bookings");
}
