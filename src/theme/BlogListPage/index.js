import React from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {
  PageMetadata,
  HtmlClassNameProvider,
  ThemeClassNames,
} from '@docusaurus/theme-common';
import BlogLayout from '@theme/BlogLayout';
import BlogListPaginator from '@theme/BlogListPaginator';
import SearchMetadata from '@theme/SearchMetadata';
import BlogPostItems from '@theme/BlogPostItems';
import styles from './styles.module.css';

function BlogListPageMetadata(props) {
  const {metadata} = props;
  const {
    siteConfig: {title: siteTitle},
  } = useDocusaurusContext();
  const {blogDescription, blogTitle, permalink} = metadata;
  const isBlogOnlyMode = permalink === '/';
  const title = isBlogOnlyMode ? siteTitle : blogTitle;
  return (
    <>
      <PageMetadata title={title} description={blogDescription} />
      <SearchMetadata tag="blog_posts_list" />
    </>
  );
}

function BlogListPageContent(props) {
  const {metadata, items} = props;
  const {blogTitle} = metadata;
  const isMainBlog = metadata.permalink === '/';
  
  return (
    <BlogLayout>
      <div className={styles.blogListContainer}>
        <header className={styles.blogListHeader}>
          <div className="container">
            <h1 className={styles.blogListTitle}>
              {isMainBlog ? 'Engineering Blog' : blogTitle}
            </h1>
            <p className={styles.blogListSubtitle}>
              {isMainBlog 
                ? 'Kiến thức, kinh nghiệm và góc nhìn về công nghệ, AI và engineering practices.'
                : 'Tin tức và cập nhật mới nhất'}
            </p>
          </div>
        </header>
        
        <div className="container margin-vert--lg">
          <div className={styles.blogListGrid}>
            <BlogPostItems items={items} />
          </div>
          <BlogListPaginator metadata={metadata} />
        </div>
      </div>
    </BlogLayout>
  );
}

export default function BlogListPage(props) {
  return (
    <HtmlClassNameProvider
      className={clsx(
        ThemeClassNames.wrapper.blogPages,
        ThemeClassNames.page.blogListPage,
      )}>
      <BlogListPageMetadata {...props} />
      <BlogListPageContent {...props} />
    </HtmlClassNameProvider>
  );
}
