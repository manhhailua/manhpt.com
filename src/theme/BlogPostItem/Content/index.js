import React from 'react';
import clsx from 'clsx';
import {useBlogPost} from '@docusaurus/plugin-content-blog/client';
import styles from './styles.module.css';

export default function BlogPostItemContent({children, className}) {
  const {isBlogPostPage} = useBlogPost();
  return (
    <div
      className={clsx(
        'markdown',
        isBlogPostPage ? styles.blogPostContent : styles.blogPostExcerpt,
        className,
      )}>
      {children}
    </div>
  );
}
