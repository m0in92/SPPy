import React, { Suspense } from 'react';

export function Container_inputs(props) {
    const lazyComponentName = window.location.pathname
  const MyLazyLoaded = React.lazy(() => import('./' + lazyComponentName).then(({ MyLazyLoaded }) => ({ default: MyLazyLoaded })),);
  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <MyLazyLoaded />
      </Suspense>
    </div>
  );

}