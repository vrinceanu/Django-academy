// Phase 1 screens and the milestone that builds each (build plan, "Screens and API").
export type Screen = { title: string; milestone: string; summary: string };

export const SCREENS: Record<string, Screen> = {
  "/learn": { title: "Dashboard", milestone: "M4", summary: "Your workshops, what is due next and your progress toward each microcredential." },
  "/learn/todo": { title: "To-do", milestone: "M4", summary: "Everything due across your workshops, soonest first." },
  "/learn/grades": { title: "Grades", milestone: "M5", summary: "Released grades and your weighted score against each pass mark." },
  "/learn/badges": { title: "Badges", milestone: "M6", summary: "Badges and certificates you have earned, ready to share or verify." },
  "/teach": { title: "Teaching home", milestone: "M4", summary: "The workshops you teach this cycle and what needs your attention." },
  "/teach/grading": { title: "Grading queue", milestone: "M5", summary: "Submissions waiting for a grade, oldest first." },
  "/studio": { title: "Packages", milestone: "M2", summary: "Content packages you author, with their latest build and publish status." },
  "/studio/media": { title: "Media library", milestone: "M3", summary: "Lecture videos, their transcode status and captions." },
  "/manage": { title: "Overview", milestone: "M4", summary: "This cycle at a glance: applications, cohorts, workshops and failed jobs." },
  "/manage/people": { title: "People", milestone: "M1", summary: "Students, instructors, authors and admins across the Network." },
  "/manage/cycles": { title: "Cycles", milestone: "M1", summary: "Network cycles and their dates." },
  "/manage/schools": { title: "Schools & MOUs", milestone: "M1", summary: "Member schools and the MOUs that recognize Network certificates." },
  "/manage/catalog": { title: "Catalog", milestone: "M2", summary: "Published microcredentials and certificates, and versions awaiting review." },
  "/manage/credentials": { title: "Credentials", milestone: "M6", summary: "Badges held for approval, issued awards and revocations." },
  "/manage/audit": { title: "Audit log", milestone: "M1", summary: "Every staff change, who made it and when." },
  "/account": { title: "Profile", milestone: "M1", summary: "Your name, school and contact preferences." },
  "/account/notifications": { title: "Notifications", milestone: "M6", summary: "Choose what reaches you by email and in the app." },
  "/account/privacy": { title: "Privacy & consents", milestone: "M1", summary: "The terms you accepted, and requests to export or delete your data." },
};
