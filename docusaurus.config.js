// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "ManhPT's Engineering Blog",
  url: "https://manhpt.com",
  baseUrl: "/",

  // The tagline for your website.
  tagline: "IT Engineering Knowledges and Experiences",

  // The behavior of Docusaurus when it detects any broken link.
  // By default, it throws an error, to ensure you never ship any broken link, but you can lower this security if needed.
  onBrokenLinks: "warn",

  // The behavior of Docusaurus when it detects any broken markdown link.
  // By default, it prints a warning, to let you know about your broken markdown link, but you can change this security if needed.
  onBrokenMarkdownLinks: "warn",

  // Path to your site favicon; must be a URL that can be used in link's href. For example, if your favicon is in static/img/favicon.ico
  favicon: "img/favicon.ico",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "manhhailua", // Usually your GitHub org/user name.
  projectName: "manhpt.com", // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "vi",
    locales: ["vi"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/manhhailua/manhpt.com/tree/master/",
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/manhhailua/manhpt.com/tree/master/",
          // URL route for the blog section of your site. DO NOT include a trailing slash.
          // Use / to put the blog at root path.
          routeBasePath: "/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: "ManhPT",
        logo: {
          alt: "ManhPT's Engineering Blog",
          src: "img/manhpt-logo-512.png",
        },
        items: [
          { to: "/", label: "Blog", position: "left" },
          { to: "/archive", label: "Archive", position: "left" },
          {
            type: "doc",
            docId: "intro",
            position: "left",
            label: "Tutorial",
          },
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
                label: "Tutorials",
                to: "/docs/intro",
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
                label: "Twitter",
                href: "https://twitter.com/manhhailua",
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
        copyright: "Built with Docusaurus.",
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
