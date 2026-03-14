import React from 'react';
import clsx from 'clsx';
import {useBlogPost} from '@docusaurus/plugin-content-blog/client';
import BlogPostItemContainer from '@theme/BlogPostItem/Container';
import BlogPostItemHeader from '@theme/BlogPostItem/Header';
import BlogPostItemContent from '@theme/BlogPostItem/Content';
import BlogPostItemFooter from '@theme/BlogPostItem/Footer';
import styles from './styles.module.css';

export default function BlogPostItem({children, className}) {
  const {metadata, isBlogPostPage} = useBlogPost();
  const {
    permalink,
    frontMatter,
  } = metadata;
  const {hide_table_of_contents: hideTableOfContents} = frontMatter;
  
  if (isBlogPostPage) {
    return (
      <BlogPostItemContainer className={clsx(className, styles.blogPostPage)}>
        <BlogPostItemHeader />
        <BlogPostItemContent>{children}</BlogPostItemContent>
        <BlogPostItemFooter />
      </BlogPostItemContainer>
    );
  }

  return (
    <BlogPostItemContainer
      as="article"
      className={clsx(className, styles.blogPostCard)}>
      <a href={permalink} className={styles.blogPostCardLink}>
        <BlogPostItemHeader />
        <BlogPostItemContent>{children}</BlogPostItemContent>
        <BlogPostItemFooter />
      </a>
    </BlogPostItemContainer>
  );
}
