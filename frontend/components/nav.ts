// Left navigation per area. Screens are added milestone by milestone (build plan).
export type NavItem = { href: string; label: string };
export type Area = { key: string; label: string; home: string; items: NavItem[] };

export const AREAS: Area[] = [
  {
    key: "learn",
    label: "Learn",
    home: "/learn",
    items: [
      { href: "/learn", label: "Dashboard" },
      { href: "/learn/todo", label: "To-do" },
      { href: "/learn/grades", label: "Grades" },
      { href: "/learn/badges", label: "Badges" },
    ],
  },
  {
    key: "teach",
    label: "Teach",
    home: "/teach",
    items: [
      { href: "/teach", label: "Teaching home" },
      { href: "/teach/grading", label: "Grading queue" },
    ],
  },
  {
    key: "studio",
    label: "Studio",
    home: "/studio",
    items: [
      { href: "/studio", label: "Packages" },
      { href: "/studio/media", label: "Media library" },
    ],
  },
  {
    key: "manage",
    label: "Manage",
    home: "/manage",
    items: [
      { href: "/manage", label: "Overview" },
      { href: "/manage/people", label: "People" },
      { href: "/manage/cycles", label: "Cycles" },
      { href: "/manage/schools", label: "Schools & MOUs" },
      { href: "/manage/catalog", label: "Catalog" },
      { href: "/manage/credentials", label: "Credentials" },
      { href: "/manage/audit", label: "Audit log" },
    ],
  },
];

export const ACCOUNT_ITEMS: NavItem[] = [
  { href: "/account", label: "Profile" },
  { href: "/account/notifications", label: "Notifications" },
  { href: "/account/privacy", label: "Privacy & consents" },
];
