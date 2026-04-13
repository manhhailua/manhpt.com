// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import { themes as prismThemes } from "prism-react-renderer";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "ManhPT's Engineering Blog — IT & AI Knowledge Hub",
  tagline:
    "IT Engineering Knowledges and Experiences. Lưu trữ kiến thức, kinh nghiệm và đôi khi là góc nhìn về công nghệ.",
  favicon: "img/favicon.ico",

  // Set the production url of your site here
  url: "https://manhpt.com",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "manhhailua", // Usually your GitHub org/user name.
  projectName: "manhpt.com", // Usually your repo name.

  onBrokenLinks: "throw",
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: "warn",
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "vi",
    locales: ["vi"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: false, // Disable the docs plugin
        blog: {
          routeBasePath: "/", // Serve the blog at the site's root
          blogTitle: "ManhPT's Engineering Blog — IT & AI Knowledge Hub",
          blogDescription:
            "IT Engineering Knowledges and Experiences. Lưu trữ kiến thức, kinh nghiệm và đôi khi là góc nhìn về công nghệ.",
          showReadingTime: true,
          feedOptions: {
            type: ["rss", "atom"],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/manhhailua/manhpt.com/tree/main/blog",
          // Useful options to enforce blogging best practices
          onInlineTags: "warn",
          onInlineAuthors: "warn",
          onUntruncatedBlogPosts: "warn",
        },
        theme: {
          customCss: "./src/css/custom.css",
        },
      }),
    ],
  ],

  plugins: [
    [
      "@docusaurus/plugin-content-blog",
      {
        /**
         * Required for any multi-instance plugin
         */
        id: "news",
        blogTitle: "ManhPT's Short Tech News — Tin tức IT & AI ngắn gọn",
        blogDescription:
          "Cập nhật nhanh các tin tức ngắn gọn về công nghệ, AI và kỹ thuật phần mềm từ góc nhìn thực chiến của một kỹ sư IT.",
        /**
         * URL route for the blog section of your site.
         * *DO NOT* include a trailing slash.
         */
        routeBasePath: "news",
        /**
         * Path to data on filesystem relative to site dir.
         */
        path: "./news",
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: "img/manhpt-og-custom-red.jpg",
      navbar: {
        title: "ManhPT",
        logo: {
          alt: "ManhPT's Engineering Blog",
          src: "img/manhpt-logo-512.png",
        },
        items: [
          { to: "/", label: "Blog", position: "left" },
          { to: "/news", label: "News", position: "left" },
          { to: "/rag-papers", label: "RAG Papers", position: "left" },
          {
            href: "https://github.com/manhhailua",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Content",
            items: [
              {
                label: "Blog",
                to: "/",
              },
              {
                label: "News",
                to: "/news",
              },
            ],
          },
          {
            title: "Community",
            items: [
              {
                label: "Linkedin",
                href: "https://www.linkedin.com/in/manhpt/",
              },
              {
                label: "Stack Overflow",
                href: "https://stackoverflow.com/users/1955725/manhhailua",
              },
              {
                label: "X",
                href: "https://x.com/manhhailua",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "GitHub",
                href: "https://github.com/manhhailua",
              },
            ],
          },
        ],
        logo: {
          alt: "ManhPT's Engineering Blog",
          src: "img/manhpt-logo-192h.png",
          href: "/",
        },
        copyright: "Powered by ManhPT | Built with Docusaurus",
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
